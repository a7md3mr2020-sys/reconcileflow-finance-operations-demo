import io

from openpyxl import Workbook, load_workbook

import app as app_module
from reconcileflow.sample_data import HEADERS, SYSTEM_A, SYSTEM_B


def csrf(client):
    with client.session_transaction() as session:
        session["csrf_token"] = "test-token"
    return "test-token"


def workbook_bytes(rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return output


def test_health_and_security_headers(client):
    response = client.get("/health")
    assert response.json == {"ok": True, "service": "ReconcileFlow"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_hub_exposes_all_three_workflows_and_report_workshop(client):
    response = client.get("/")
    assert response.status_code == 200
    for label in (b"Standard Reconciliation", b"Detailed Reconciliation", b"Invoice Tracking", b"Report Workshop"):
        assert label in response.data


def test_complete_demo_workflow_and_export(client):
    response = client.post("/demo", data={"csrf_token": csrf(client)}, follow_redirects=False)
    assert response.status_code == 302
    result_url = response.headers["Location"]
    page = client.get(result_url)
    assert page.status_code == 200
    assert b"13" in page.data
    assert b"Duplicate detected" in page.data
    export = client.get(result_url + "/export.xlsx")
    assert export.status_code == 200
    workbook = load_workbook(io.BytesIO(export.data), read_only=True, data_only=True)
    assert workbook.sheetnames == ["Summary", "Reconciliation Results", "Company Mappings"]
    assert workbook["Reconciliation Results"].max_row == 14
    assert workbook["Reconciliation Results"]["A2"].value == "RF-1001"
    assert workbook["Reconciliation Results"].max_column == 20
    workbook.close()


def test_upload_validation_returns_friendly_error(client):
    response = client.post(
        "/reconcile",
        data={
            "csrf_token": csrf(client),
            "project_name": "Invalid upload",
            "system_a": (io.BytesIO(b"not excel"), "a.xlsx"),
            "system_b": (io.BytesIO(b"not excel"), "b.xlsx"),
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert b"invalid Excel file" in response.data


def test_valid_excel_upload_runs_reconciliation(client):
    response = client.post(
        "/reconcile",
        data={
            "csrf_token": csrf(client),
            "project_name": "Uploaded synthetic review",
            "system_a": (workbook_bytes(SYSTEM_A), "a.xlsx"),
            "system_b": (workbook_bytes(SYSTEM_B), "b.xlsx"),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Uploaded synthetic review" in response.data
    assert b"15.4%" in response.data


def test_sample_downloads_and_excel_cell_protection(client):
    response = client.get("/sample-data/a.xlsx")
    assert response.status_code == 200
    workbook = load_workbook(io.BytesIO(response.data), read_only=True, data_only=True)
    assert workbook.active.max_row == 14
    workbook.close()
    assert app_module.excel_safe("=2+2") == "'=2+2"
    assert app_module.excel_safe("Normal label") == "Normal label"


def test_csrf_is_required(client):
    response = client.post("/demo", data={})
    assert response.status_code == 400


def test_unknown_result_is_404(client):
    assert client.get("/results/unknown").status_code == 404


def test_detailed_demo_and_export(client):
    response = client.post("/detailed/demo", data={"csrf_token": csrf(client)}, follow_redirects=False)
    assert response.status_code == 302
    page = client.get(response.headers["Location"])
    assert page.status_code == 200
    assert b"Reference-number reconciliation" in page.data
    assert b"Hotel or pickup" in page.data
    export = client.get(response.headers["Location"] + "/export.xlsx")
    workbook = load_workbook(io.BytesIO(export.data), read_only=True, data_only=True)
    assert workbook.sheetnames == ["Summary", "Detailed Results", "Reference Matching"]
    assert workbook["Detailed Results"].max_row == 8
    workbook.close()


def test_invoice_tracking_views_export_and_workshop(client):
    for tab in ("overview", "companies", "analysis", "activity"):
        response = client.get(f"/invoice-tracking?tab={tab}")
        assert response.status_code == 200
        assert b"Marine operations invoice follow-up" in response.data
    export = client.get("/invoice-tracking/export.xlsx")
    workbook = load_workbook(io.BytesIO(export.data), read_only=True, data_only=True)
    assert workbook.sheetnames == ["Summary", "Company Tracking", "Activity Log"]
    assert workbook["Company Tracking"].max_row == 8
    workbook.close()
    workshop = client.get("/report-workshop")
    assert workshop.status_code == 200
    assert b"Visible identity" in workshop.data
    assert b"Authorized signature and stamp" in workshop.data


def test_operations_control_center_views_and_export(client):
    expected = {
        "overview": b"Four periods acting as one workspace",
        "companies": b"Unified company groups across projects",
        "settlements": b"Settlement movement ledger",
        "no-shows": b"Whole and partial booking evidence",
        "delivery": b"Delivery and approved statement readiness",
    }
    for tab, marker in expected.items():
        response = client.get(f"/control-center?tab={tab}")
        assert response.status_code == 200
        assert marker in response.data

    export = client.get("/control-center/export.xlsx")
    assert export.status_code == 200
    workbook = load_workbook(io.BytesIO(export.data), read_only=True, data_only=True)
    assert workbook.sheetnames == [
        "Executive Summary", "Projects", "Unified Companies", "Settlement Ledger",
        "No Shows", "Delivery Control",
    ]
    assert workbook["Unified Companies"].max_row == 6
    assert workbook["Settlement Ledger"].max_row == 6
    assert workbook["No Shows"]["H5"].value == 210
    workbook.close()


import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE_PATH", tmp_path / "test.db")
    app_module.init_database()
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-key")
    with app_module.app.test_client() as test_client:
        yield test_client
