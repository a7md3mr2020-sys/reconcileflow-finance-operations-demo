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
