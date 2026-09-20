import io

import pytest
from openpyxl import Workbook

from reconcileflow.engine import canonical_company, read_dataset, reconcile
from reconcileflow.sample_data import HEADERS, SYSTEM_A, SYSTEM_B, records


def workbook_bytes(headers=HEADERS, rows=None):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(headers)
    for row in rows or [SYSTEM_A[0]]:
        sheet.append(row)
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return output


def test_synthetic_demo_covers_every_outcome():
    payload = reconcile(records(SYSTEM_A), records(SYSTEM_B))
    assert payload["summary"] == {
        "total": 13,
        "matched": 2,
        "mismatch": 8,
        "missing_a": 1,
        "missing_b": 1,
        "duplicates": 1,
        "match_rate": 15.4,
        "system_a_rows": 13,
        "system_b_rows": 12,
        "amount_variance": 150.0,
    }
    assert {row["status"] for row in payload["results"]} == {
        "matched", "mismatch", "missing_a", "missing_b", "duplicate"
    }


def test_company_aliases_are_normalized_without_hiding_original_labels():
    assert canonical_company("RedSea Tours") == "RED SEA TOURS"
    payload = reconcile(records(SYSTEM_A[:2]), records(SYSTEM_B[:2]))
    assert all(row["status"] == "matched" for row in payload["results"])
    assert payload["mappings"][0]["system_a"] != payload["mappings"][0]["system_b"]


def test_excel_reader_parses_valid_workbook():
    parsed = read_dataset(workbook_bytes(), "system-a.xlsx")
    assert parsed[0]["reference"] == "RF 1001"
    assert parsed[0]["amount"] == 250.0


def test_excel_reader_rejects_missing_headers():
    with pytest.raises(ValueError, match="Missing required columns"):
        read_dataset(workbook_bytes(headers=["Reference", "Date"]), "broken.xlsx")


def test_excel_reader_rejects_invalid_numeric_value():
    row = list(SYSTEM_A[0])
    row[-1] = "not-a-number"
    with pytest.raises(ValueError, match="amount must be numeric"):
        read_dataset(workbook_bytes(rows=[row]), "broken.xlsx")


def test_blank_references_keep_separate_daily_company_balances():
    first = list(SYSTEM_A[0])
    second = list(SYSTEM_A[0])
    first[0] = ""
    second[0] = None
    second[2] = "Other Company"
    parsed = read_dataset(workbook_bytes(rows=[first, second]), "blank-reference.xlsx")
    assert [row["reference"] for row in parsed] == ["0", "0"]
    payload = reconcile(parsed, [])
    assert len(payload["daily_results"]) == 2
    assert sum(row["variance"] for row in payload["daily_results"]) == 500
    assert all(row["status"] == "missing_b" for row in payload["daily_results"])


def test_daily_matching_aggregates_different_references_for_same_company_day():
    left = records(SYSTEM_A[:1]) + records(SYSTEM_A[:1])
    left[1]["reference"] = "OTHER"
    right = records(SYSTEM_B[:1]) + records(SYSTEM_B[:1])
    right[1]["reference"] = "DIFFERENT"
    payload = reconcile(left, right)
    assert len(payload["daily_results"]) == 1
    row = payload["daily_results"][0]
    assert row["status"] == "matched"
    assert row["rows_a"] == row["rows_b"] == 2
    assert row["amount_a"] == row["amount_b"] == 500


def test_arabic_company_name_is_preserved_for_matching():
    row = list(SYSTEM_A[0])
    row[2] = "شركة البحر الأحمر"
    parsed = read_dataset(workbook_bytes(rows=[row]), "arabic-company.xlsx")
    assert parsed[0]["company_canonical"] == "شركة البحر الأحمر"
