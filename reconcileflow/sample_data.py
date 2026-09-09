from __future__ import annotations

from reconcileflow.engine import canonical_company, normalize


HEADERS = ["Reference", "Date", "Company", "Service", "Adult", "Child", "Infant", "Amount"]

SYSTEM_A = [
    ["RF-1001", "2026-08-01", "Nile Horizon Travel", "Orange Bay", 2, 1, 0, 250],
    ["RF-1002", "2026-08-01", "Red Sea Tours LLC", "Dolphin House", 2, 0, 0, 220],
    ["RF-1003", "2026-08-02", "Blue Wave Travel", "Paradise Island", 3, 1, 0, 360],
    ["RF-1004", "2026-08-02", "Sunrise Holidays", "City Tour", 2, 2, 0, 180],
    ["RF-1005", "2026-08-03", "Coral Gate Tourism", "Glass Boat", 2, 0, 1, 160],
    ["RF-1006", "2026-08-03", "Desert Star Travel", "Safari", 4, 1, 0, 410],
    ["RF-1007", "2026-08-04", "Nile Horizon Travel", "Orange Bay", 2, 0, 0, 200],
    ["RF-1009", "2026-08-05", "Blue Wave Travel", "Dolphin House", 1, 0, 0, 110],
    ["RF-1009", "2026-08-05", "Blue Wave Travel", "Dolphin House", 1, 0, 0, 110],
    ["RF-1010", "2026-08-06", "Sunrise Holidays", "City Tour", 2, 0, 0, 140],
    ["RF-1011", "2026-08-06", "Coral Gate Tourism", "Glass Boat", 2, 1, 0, 210],
    ["RF-1012", "2026-08-07", "Desert Star Travel", "Safari", 3, 0, 0, 300],
    ["RF-1013", "2026-08-07", "Nile Horizon Travel", "Orange Bay", 4, 2, 0, 500],
]

SYSTEM_B = [
    ["RF-1001", "2026-08-01", "Nile Horizon Travel Co", "Orange Bay", 2, 1, 0, 250],
    ["RF-1002", "2026-08-01", "Red Sea Tours", "Dolphin House", 2, 0, 0, 220],
    ["RF-1003", "2026-08-02", "BlueWave Travel", "Paradise Island", 2, 1, 0, 360],
    ["RF-1004", "2026-08-02", "Sunrise Holidays", "City Tour", 2, 1, 0, 180],
    ["RF-1005", "2026-08-03", "Coral Gate Tourism", "Glass Boat", 2, 0, 0, 160],
    ["RF-1006", "2026-08-03", "Desert Star Travel", "Safari", 4, 1, 0, 390],
    ["RF-1008", "2026-08-04", "Red Sea Tours", "Dolphin House", 2, 0, 0, 220],
    ["RF-1009", "2026-08-05", "Blue Wave Travel", "Dolphin House", 1, 0, 0, 110],
    ["RF-1010", "2026-08-07", "Sunrise Holidays", "City Tour", 2, 0, 0, 140],
    ["RF-1011", "2026-08-06", "Coral Gate Tourism", "Semi Submarine", 2, 1, 0, 210],
    ["RF-1012", "2026-08-07", "Coastal Journey Group", "Safari", 3, 0, 0, 300],
    ["RF-1013", "2026-08-08", "Nile Horizon Travel", "Dolphin House", 3, 1, 1, 460],
]


def records(rows):
    return [
        {
            "reference": row[0],
            "date": row[1],
            "company": row[2],
            "company_canonical": canonical_company(row[2]),
            "service": row[3],
            "service_normalized": normalize(row[3]),
            "adult": float(row[4]),
            "child": float(row[5]),
            "infant": float(row[6]),
            "amount": float(row[7]),
        }
        for row in rows
    ]
