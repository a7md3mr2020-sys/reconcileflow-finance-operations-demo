from __future__ import annotations

from collections import defaultdict


STATUS_LABELS = {
    "matched": "Matched",
    "missing_a": "System B only",
    "missing_b": "System A only",
    "amount_only": "Amount difference",
    "pax_only": "Passenger difference",
    "amount_and_pax": "Amount and passenger difference",
}


def daily_matches(system_a, system_b, detailed=False, tolerance=0.01):
    """Mirror the original project's day/company(/trip) reconciliation grain."""
    groups = defaultdict(lambda: {"system_a": [], "system_b": []})
    for side, rows in (("system_a", system_a), ("system_b", system_b)):
        for row in rows:
            key = (row["date"], row["company_canonical"])
            if detailed:
                key += (row["service_normalized"],)
            groups[key][side].append(row)

    results = []
    for key, sides in sorted(groups.items()):
        left, right = sides["system_a"], sides["system_b"]
        all_rows = left + right
        def total(rows, field):
            return round(sum(float(row.get(field, 0) or 0) for row in rows), 2)

        amount_a, amount_b = total(left, "amount"), total(right, "amount")
        variance = round(amount_a - amount_b, 2)
        chargeable_a, chargeable_b = total(left, "chargeable_pax"), total(right, "chargeable_pax")
        calculated_a, calculated_b = total(left, "calculated_amount"), total(right, "calculated_amount")
        pickup_a = ", ".join(sorted({row.get("pickup", "") for row in left if row.get("pickup")}))
        pickup_b = ", ".join(sorted({row.get("pickup", "") for row in right if row.get("pickup")}))
        pax = {
            field: (total(left, field), total(right, field))
            for field in ("adult", "child", "infant")
        }
        pax_diff = any(abs(a - b) > 1e-9 for field, (a, b) in pax.items() if field != "infant")
        amount_diff = abs(variance) >= tolerance
        if not left:
            status = "missing_a"
        elif not right:
            status = "missing_b"
        elif amount_diff and pax_diff:
            status = "amount_and_pax"
        elif amount_diff:
            status = "amount_only"
        elif pax_diff:
            status = "pax_only"
        else:
            status = "matched"
        results.append({
            "date": key[0],
            "company": all_rows[0]["company"],
            "project_name": ", ".join(dict.fromkeys(row["project_name"] for row in all_rows if row.get("project_name"))),
            "trip": all_rows[0]["service"] if detailed else "",
            "references_a": ", ".join(sorted({row.get("reference", "0") for row in left})),
            "references_b": ", ".join(sorted({row.get("reference", "0") for row in right})),
            "rows_a": sum(row.get("row_count", 1) for row in left),
            "rows_b": sum(row.get("row_count", 1) for row in right),
            "amount_a": amount_a, "amount_b": amount_b, "variance": variance,
            "adult_a": pax["adult"][0], "adult_b": pax["adult"][1],
            "child_a": pax["child"][0], "child_b": pax["child"][1],
            "infant_a": pax["infant"][0], "infant_b": pax["infant"][1],
            "pickup_a": pickup_a, "pickup_b": pickup_b,
            "transfer_a": sum(bool(row.get("has_transfer")) for row in left),
            "transfer_b": sum(bool(row.get("has_transfer")) for row in right),
            "chargeable_a": chargeable_a, "chargeable_b": chargeable_b,
            "rate_a": round(calculated_a / chargeable_a, 4) if chargeable_a else 0,
            "rate_b": round(calculated_b / chargeable_b, 4) if chargeable_b else 0,
            "calculated_a": calculated_a, "calculated_b": calculated_b,
            "calculated_variance": round(calculated_a - calculated_b, 2),
            "pricing_variance_a": total(left, "pricing_variance"),
            "pricing_variance_b": total(right, "pricing_variance"),
            "status": status, "status_label": STATUS_LABELS[status],
        })
    return results
