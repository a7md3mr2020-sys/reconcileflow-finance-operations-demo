import io

from openpyxl import Workbook

from reconcileflow.detailed import finalize_record, read_detailed_dataset, reconcile_detailed
from reconcileflow.extended_sample_data import DETAILED_A, DETAILED_B, DETAILED_HEADERS, detailed_records


def test_detailed_demo_covers_pricing_and_reference_outcomes():
    payload = reconcile_detailed(detailed_records(DETAILED_A), detailed_records(DETAILED_B))
    assert payload["summary"] == {
        "total": 7, "matched": 1, "mismatch": 3, "missing_a": 1, "missing_b": 1,
        "duplicates": 1, "match_rate": 14.3, "amount_variance": 32.5,
        "pricing_variance_a": 0.0, "pricing_variance_b": 0.0,
    }


def test_rate_and_amount_are_derived_using_chargeable_passengers():
    base = {"reference": "A-1", "date": "2026-08-01", "company": "Demo", "service": "Trip", "pickup": "", "adult": 2, "child": 1, "infant": 2}
    from_amount = finalize_record({**base, "adult_rate": "", "amount": 300}, 2)
    assert from_amount["chargeable_pax"] == 2.5
    assert from_amount["adult_rate"] == 120
    assert from_amount["has_transfer"] is False
    from_rate = finalize_record({**base, "adult_rate": 120, "amount": ""}, 2)
    assert from_rate["amount"] == 300


def test_detailed_excel_reader_accepts_expected_template():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(DETAILED_HEADERS)
    sheet.append(DETAILED_A[0])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    parsed = read_detailed_dataset(output, "detailed.xlsx")
    assert parsed[0]["adult_rate"] == 120


def test_detailed_daily_matching_separates_trip_types_at_same_company_and_date():
    base = {"reference": "", "date": "2026-08-01", "company": "Demo", "pickup": "", "adult": 2, "child": 0, "infant": 0, "adult_rate": 100, "amount": 200}
    left = [finalize_record({**base, "service": "Island"}), finalize_record({**base, "service": "Reef"})]
    right = [finalize_record({**base, "service": "Island"})]
    payload = reconcile_detailed(left, right)
    assert len(payload["daily_results"]) == 2
    assert {row["trip"]: row["status"] for row in payload["daily_results"]} == {"Island": "matched", "Reef": "missing_b"}
    island = next(row for row in payload["daily_results"] if row["trip"] == "Island")
    assert island["chargeable_a"] == island["chargeable_b"] == 2
    assert island["rate_a"] == island["rate_b"] == 100
    assert island["calculated_a"] == island["calculated_b"] == 200
    assert island["calculated_variance"] == 0
