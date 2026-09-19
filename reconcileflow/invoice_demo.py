from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


STAGES = ("waiting", "matched", "prepared", "sent", "paid")


def amount_to_minor(value):
    try:
        amount = Decimal(str(value).strip().replace(",", ""))
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid amount.") from None
    if not amount.is_finite() or not 0 <= amount <= Decimal("999999999.99"):
        raise ValueError("Amount must be between 0 and 999,999,999.99.")
    return int(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)


def invoice_view(company_rows, event_rows, search="", direction=""):
    companies = []
    invoice_minor = collected_minor = receivable_minor = payable_minor = 0
    search = search.strip().casefold()
    direction = direction if direction in {"receivable", "payable", "settled"} else ""
    for record in company_rows:
        row = dict(record)
        balance_minor = row["invoice_minor"] - row["paid_minor"] - row["payment_minor"]
        row_direction = "receivable" if balance_minor > 0 else "payable" if balance_minor < 0 else "settled"
        if direction and row_direction != direction:
            continue
        if search and search not in " ".join((row["code"], row["name"], row["notes"])).casefold():
            continue
        invoice_minor += row["invoice_minor"]
        collected_minor += row["paid_minor"] + row["payment_minor"]
        receivable_minor += max(balance_minor, 0)
        payable_minor += max(-balance_minor, 0)
        companies.append({
            "code": row["code"], "name": row["name"], "stage": row["stage"], "notes": row["notes"],
            "invoice": row["invoice_minor"] / 100, "paid": row["paid_minor"] / 100,
            "payment": row["payment_minor"] / 100, "balance": balance_minor / 100,
            "direction": row_direction,
            "progress": STAGES.index(row["stage"]) * 25,
        })
    visible_codes = {row["code"] for row in companies}
    activities = [{
        "time": row["occurred_at"][:16].replace("T", " "), "company": row["company_name"],
        "action": row["action"], "before": row["before_minor"] / 100,
        "after": row["after_minor"] / 100,
    } for row in event_rows if row["company_code"] in visible_codes]
    return {
        "companies": companies,
        "activities": activities,
        "summary": {
            "companies": len(companies), "invoice": invoice_minor / 100,
            "collected": collected_minor / 100, "receivable": receivable_minor / 100,
            "payable": payable_minor / 100, "net": (receivable_minor - payable_minor) / 100,
            "collection_rate": round(collected_minor * 100 / invoice_minor, 1) if invoice_minor else 0,
            "completed": sum(row["stage"] == "paid" for row in companies),
        },
    }
