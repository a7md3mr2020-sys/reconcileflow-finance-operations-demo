from __future__ import annotations


PROJECTS = [
    {"name": "May Operations", "period": "May 2026", "progress": 100, "companies": 18, "open": 0, "receivable": 0, "payable": 0},
    {"name": "June Operations", "period": "June 2026", "progress": 92, "companies": 21, "open": 4, "receivable": 18450, "payable": 3200},
    {"name": "July Operations", "period": "July 2026", "progress": 78, "companies": 24, "open": 11, "receivable": 36750, "payable": 8900},
    {"name": "August Operations", "period": "August 2026", "progress": 61, "companies": 20, "open": 17, "receivable": 49200, "payable": 6400},
]

COMPANY_LINKS = [
    {"canonical": "Nile Horizon Travel", "system_a": "Nile Horizon / Nile Horizon Travel", "system_b": "Nile Horizon Co / NH Travel", "projects": 4, "aliases": 4, "confidence": 98, "status": "approved"},
    {"canonical": "Red Sea Tours", "system_a": "Red Sea Tours LLC / Red Sea", "system_b": "RST / Red Sea Tours", "projects": 4, "aliases": 4, "confidence": 96, "status": "approved"},
    {"canonical": "Blue Wave Travel", "system_a": "Blue Wave / BlueWave", "system_b": "Blue Wave Travel", "projects": 3, "aliases": 3, "confidence": 93, "status": "approved"},
    {"canonical": "Coral Gate Tourism", "system_a": "Coral Gate", "system_b": "Coral Gate Tourism / CGT", "projects": 2, "aliases": 3, "confidence": 87, "status": "review"},
    {"canonical": "Coastal Journey Group", "system_a": "Not present in August", "system_b": "Coastal Journey / CJ Group", "projects": 2, "aliases": 2, "confidence": 74, "status": "review"},
]

SETTLEMENTS = [
    {"date": "2026-08-14", "time": "15:40", "project": "August Operations", "reference": "RF-2841", "company": "Nile Horizon Travel", "action": "Booking amount corrected", "before": 4200, "after": 3900, "movement": 300, "status": "decrease"},
    {"date": "2026-08-14", "time": "13:25", "project": "August Operations", "reference": "RF-2798", "company": "Red Sea Tours", "action": "Additional service restored", "before": 1850, "after": 2050, "movement": -200, "status": "increase"},
    {"date": "2026-08-13", "time": "17:10", "project": "July Operations", "reference": "RF-2554", "company": "Blue Wave Travel", "action": "Deleted duplicate booking", "before": 1600, "after": 0, "movement": 1600, "status": "deletion"},
    {"date": "2026-08-13", "time": "11:05", "project": "July Operations", "reference": "RF-2493", "company": "Coral Gate Tourism", "action": "Child count correction", "before": 1100, "after": 950, "movement": 150, "status": "decrease"},
    {"date": "2026-08-12", "time": "16:30", "project": "June Operations", "reference": "RF-2188", "company": "Nile Horizon Travel", "action": "Manual agreement posted", "before": 700, "after": 0, "movement": 700, "status": "agreement"},
]

NO_SHOWS = [
    {"reference": "NS-3101", "date": "2026-08-12", "company": "Nile Horizon Travel", "shape": "Missing from partner source", "adult": 2, "child": 1, "infant": 0, "value": 625, "resolution": "manual", "status": "confirmed"},
    {"reference": "NS-3108", "date": "2026-08-12", "company": "Red Sea Tours", "shape": "Partial passenger no-show", "adult": 1, "child": 1, "infant": 0, "value": 360, "resolution": "manual", "status": "confirmed"},
    {"reference": "NS-3122", "date": "2026-08-13", "company": "Blue Wave Travel", "shape": "Partner price is zero", "adult": 2, "child": 0, "infant": 1, "value": 440, "resolution": "automatic", "status": "confirmed"},
    {"reference": "NS-3140", "date": "2026-08-14", "company": "Coral Gate Tourism", "shape": "Present in both sources", "adult": 1, "child": 0, "infant": 0, "value": 210, "resolution": "review", "status": "review"},
]

RESOLUTIONS = [
    {"company": "Nile Horizon Travel", "automatic": 138, "agreement": 9, "open": 4, "resolved_value": 28450, "open_value": 3200},
    {"company": "Red Sea Tours", "automatic": 121, "agreement": 6, "open": 2, "resolved_value": 21700, "open_value": 1150},
    {"company": "Blue Wave Travel", "automatic": 94, "agreement": 11, "open": 5, "resolved_value": 18900, "open_value": 4600},
    {"company": "Coral Gate Tourism", "automatic": 76, "agreement": 4, "open": 8, "resolved_value": 14350, "open_value": 7950},
]

DELIVERIES = [
    {"company": "Nile Horizon Travel", "project": "August Operations", "bookings": 151, "invoice": 125000, "delivered_on": "2026-08-15", "status": "delivered"},
    {"company": "Red Sea Tours", "project": "August Operations", "bookings": 129, "invoice": 88000, "delivered_on": "2026-08-15", "status": "delivered"},
    {"company": "Blue Wave Travel", "project": "August Operations", "bookings": 110, "invoice": 72000, "delivered_on": "", "status": "ready"},
    {"company": "Coral Gate Tourism", "project": "August Operations", "bookings": 88, "invoice": 49500, "delivered_on": "", "status": "pending"},
    {"company": "Coastal Journey Group", "project": "August Operations", "bookings": 74, "invoice": 41000, "delivered_on": "", "status": "pending"},
]


def control_center_payload():
    receivable = sum(project["receivable"] for project in PROJECTS)
    payable = sum(project["payable"] for project in PROJECTS)
    no_show_value = sum(item["value"] for item in NO_SHOWS)
    resolved_count = sum(item["automatic"] + item["agreement"] for item in RESOLUTIONS)
    open_count = sum(item["open"] for item in RESOLUTIONS)
    delivered = sum(item["status"] == "delivered" for item in DELIVERIES)
    return {
        "projects": PROJECTS,
        "company_links": COMPANY_LINKS,
        "settlements": SETTLEMENTS,
        "no_shows": NO_SHOWS,
        "resolutions": RESOLUTIONS,
        "deliveries": DELIVERIES,
        "summary": {
            "projects": len(PROJECTS),
            "companies": max(project["companies"] for project in PROJECTS),
            "progress": round(sum(project["progress"] for project in PROJECTS) / len(PROJECTS)),
            "receivable": receivable,
            "payable": payable,
            "net": receivable - payable,
            "settlement_movement": sum(item["movement"] for item in SETTLEMENTS),
            "no_show_bookings": len(NO_SHOWS),
            "no_show_value": no_show_value,
            "resolved": resolved_count,
            "open": open_count,
            "delivered": delivered,
            "delivery_total": len(DELIVERIES),
        },
    }
