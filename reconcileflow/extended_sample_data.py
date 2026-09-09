from reconcileflow.detailed import finalize_record


DETAILED_HEADERS = [
    "Reference", "Date", "Company", "Trip Type", "Hotel / Pickup",
    "Adult", "Child", "Infant", "Adult Rate", "Amount",
]

DETAILED_A = [
    ["DR-2001", "2026-08-10", "Nile Horizon Travel", "Orange Bay", "Marina Resort", 2, 1, 0, "", 300],
    ["DR-2002", "2026-08-10", "Red Sea Tours LLC", "Dolphin House", "", 2, 0, 0, 110, 220],
    ["DR-2003", "2026-08-11", "Blue Wave Travel", "Paradise Island", "Coral Hotel", 3, 1, 0, 100, 350],
    ["DR-2004", "2026-08-11", "Sunrise Holidays", "City Tour", "Sunrise Point", 2, 2, 0, 70, 210],
    ["DR-2005", "2026-08-12", "Coral Gate Tourism", "Glass Boat", "Harbour Hotel", 2, 0, 1, 80, 160],
    ["DR-2007", "2026-08-13", "Desert Star Travel", "Safari", "Desert Gate", 2, 0, 0, 100, 200],
    ["DR-2007", "2026-08-13", "Desert Star Travel", "Safari", "Desert Gate", 1, 0, 0, 100, 100],
]

DETAILED_B = [
    ["DR-2001", "2026-08-10", "Nile Horizon Travel Co", "Orange Bay", "Marina Resort", 2, 1, 0, 120, 300],
    ["DR-2002", "2026-08-10", "Red Sea Tours", "Dolphin House", "Sea View Hotel", 2, 0, 0, 110, 220],
    ["DR-2003", "2026-08-11", "BlueWave Travel", "Paradise Island", "Coral Hotel", 3, 1, 0, 95, 332.5],
    ["DR-2004", "2026-08-11", "Sunrise Holidays", "City Tour", "Sunrise Point", 2, 1, 0, 70, 175],
    ["DR-2006", "2026-08-12", "Coastal Journey Group", "Semi Submarine", "Port Hotel", 2, 0, 0, 90, 180],
    ["DR-2007", "2026-08-13", "Desert Star Travel", "Safari", "Desert Gate", 3, 0, 0, 100, 300],
]


def detailed_records(rows):
    return [finalize_record(dict(zip(
        ("reference", "date", "company", "service", "pickup", "adult", "child", "infant", "adult_rate", "amount"), row
    )), index + 2) for index, row in enumerate(rows)]


INVOICE_COMPANIES = [
    {"code": "CMP-001", "name": "Nile Horizon Travel", "invoice": 125000, "paid": 90000, "payment": 5000, "stage": "sent", "notes": "Payment confirmation pending"},
    {"code": "CMP-002", "name": "Red Sea Tours", "invoice": 88000, "paid": 88000, "payment": 0, "stage": "paid", "notes": "Cycle completed"},
    {"code": "CMP-003", "name": "Blue Wave Travel", "invoice": 72000, "paid": 80000, "payment": 0, "stage": "paid", "notes": "Credit balance under review"},
    {"code": "CMP-004", "name": "Sunrise Holidays", "invoice": 64000, "paid": 24000, "payment": 10000, "stage": "prepared", "notes": "Invoice pack prepared"},
    {"code": "CMP-005", "name": "Coral Gate Tourism", "invoice": 49500, "paid": 0, "payment": 0, "stage": "matched", "notes": "Reconciliation approved"},
    {"code": "CMP-006", "name": "Desert Star Travel", "invoice": 33000, "paid": 18000, "payment": 15000, "stage": "paid", "notes": "Settled"},
    {"code": "CMP-007", "name": "Coastal Journey Group", "invoice": 41000, "paid": 0, "payment": 0, "stage": "waiting", "notes": "Awaiting reconciliation"},
]


def invoice_payload():
    companies = []
    stage_steps = {"waiting": 0, "matched": 1, "prepared": 2, "sent": 3, "paid": 4}
    for item in INVOICE_COMPANIES:
        row = dict(item)
        row["balance"] = row["invoice"] - row["paid"] - row["payment"]
        row["direction"] = "receivable" if row["balance"] > 0 else "payable" if row["balance"] < 0 else "settled"
        row["progress"] = stage_steps[row["stage"]] * 25
        companies.append(row)
    invoice_total = sum(row["invoice"] for row in companies)
    collected = sum(row["paid"] + row["payment"] for row in companies)
    receivable = sum(max(row["balance"], 0) for row in companies)
    payable = sum(max(-row["balance"], 0) for row in companies)
    return {
        "companies": companies,
        "summary": {
            "companies": len(companies), "invoice": invoice_total, "collected": collected,
            "receivable": receivable, "payable": payable, "net": receivable - payable,
            "collection_rate": round(collected * 100 / invoice_total, 1),
            "completed": sum(row["stage"] == "paid" for row in companies),
        },
        "activities": [
            {"time": "2026-08-14 15:40", "company": "Red Sea Tours", "action": "Payment confirmed", "before": 12000, "after": 0},
            {"time": "2026-08-14 13:25", "company": "Nile Horizon Travel", "action": "Additional payment recorded", "before": 35000, "after": 30000},
            {"time": "2026-08-13 17:10", "company": "Coral Gate Tourism", "action": "Reconciliation approved", "before": 49500, "after": 49500},
            {"time": "2026-08-13 11:05", "company": "Blue Wave Travel", "action": "Invoice amount reviewed", "before": -3000, "after": -8000},
        ],
    }
