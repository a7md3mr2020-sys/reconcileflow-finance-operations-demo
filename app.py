from __future__ import annotations

import io
import json
import os
import secrets
import sqlite3
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from werkzeug.middleware.proxy_fix import ProxyFix

from reconcileflow.engine import read_dataset, reconcile
from reconcileflow.detailed import read_detailed_dataset, reconcile_detailed
from reconcileflow.control_center import control_center_payload
from reconcileflow.extended_sample_data import (
    DETAILED_A,
    DETAILED_B,
    DETAILED_HEADERS,
    detailed_records,
    invoice_payload,
)
from reconcileflow.sample_data import HEADERS, SYSTEM_A, SYSTEM_B, records


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("DEMO_DB_PATH", BASE_DIR / "instance" / "reconcileflow-demo.db"))
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 50 * 1024 * 1024
RUN_RETENTION_HOURS = int(os.environ.get("RUN_RETENTION_HOURS", "24"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    MAX_CONTENT_LENGTH=MAX_UPLOAD_BYTES,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


def database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with database() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS demo_runs(
                   id TEXT PRIMARY KEY,
                   project_name TEXT NOT NULL,
                   payload_json TEXT NOT NULL,
                   created_at TEXT NOT NULL
               )"""
        )


def store_run(project_name, payload):
    run_id = uuid4().hex
    with database() as connection:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=RUN_RETENTION_HOURS)).isoformat()
        connection.execute("DELETE FROM demo_runs WHERE created_at < ?", (cutoff,))
        connection.execute(
            "INSERT INTO demo_runs(id,project_name,payload_json,created_at) VALUES(?,?,?,?)",
            (run_id, project_name[:120], json.dumps(payload, separators=(",", ":")), datetime.now(timezone.utc).isoformat()),
        )
    return run_id


def get_run(run_id):
    with database() as connection:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=RUN_RETENTION_HOURS)).isoformat()
        connection.execute("DELETE FROM demo_runs WHERE created_at < ?", (cutoff,))
        row = connection.execute("SELECT * FROM demo_runs WHERE id=?", (run_id,)).fetchone()
    if not row:
        return None
    return {"id": row["id"], "project_name": row["project_name"], "created_at": row["created_at"], **json.loads(row["payload_json"])}


def validate_file(upload):
    if not upload or not upload.filename:
        raise ValueError("Select both System A and System B files.")
    suffix = Path(upload.filename).suffix.lower()
    if suffix not in {".xlsx", ".csv"}:
        raise ValueError("Only XLSX and CSV files are accepted.")
    upload.stream.seek(0, os.SEEK_END)
    size = upload.stream.tell()
    upload.stream.seek(0)
    if size <= 0:
        raise ValueError(f"{upload.filename}: the file is empty.")
    if size > MAX_UPLOAD_BYTES:
        raise ValueError(f"{upload.filename}: the file exceeds the 5 MB demo limit.")
    if suffix == ".xlsx":
        if not zipfile.is_zipfile(upload.stream):
            upload.stream.seek(0)
            raise ValueError(f"{upload.filename}: invalid Excel file.")
        upload.stream.seek(0)
        with zipfile.ZipFile(upload.stream) as archive:
            uncompressed_size = sum(item.file_size for item in archive.infolist())
            if uncompressed_size > MAX_UNCOMPRESSED_BYTES:
                raise ValueError(f"{upload.filename}: expanded workbook is too large for the public demo.")
    upload.stream.seek(0)


def excel_safe(value):
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def format_export_sheet(sheet, widths):
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="173E47")
        cell.alignment = Alignment(horizontal="center")
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(24)
    return session["csrf_token"]


@app.before_request
def protect_posts():
    if request.method == "POST":
        expected = session.get("csrf_token")
        submitted = request.form.get("csrf_token")
        if not expected or not submitted or not secrets.compare_digest(expected, submitted):
            abort(400, description="The form expired. Refresh the page and try again.")


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; script-src 'self'; "
        "img-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self'"
    )
    if request.path.startswith("/results") or request.method == "POST":
        response.headers["Cache-Control"] = "no-store"
    return response


app.jinja_env.globals["csrf_token"] = csrf_token
init_database()


@app.get("/")
def hub():
    return render_template("hub.html")


@app.get("/standard")
def index():
    return render_template("index.html")


@app.post("/demo")
def load_demo():
    payload = reconcile(records(SYSTEM_A), records(SYSTEM_B))
    run_id = store_run("Synthetic marine-tour operations demo", payload)
    return redirect(url_for("results", run_id=run_id))


@app.post("/reconcile")
def upload_and_reconcile():
    try:
        system_a_file = request.files.get("system_a")
        system_b_file = request.files.get("system_b")
        validate_file(system_a_file)
        validate_file(system_b_file)
        system_a = read_dataset(system_a_file.stream, system_a_file.filename)
        system_b = read_dataset(system_b_file.stream, system_b_file.filename)
        payload = reconcile(system_a, system_b)
        run_id = store_run(request.form.get("project_name", "").strip() or "Reconciliation review", payload)
        return redirect(url_for("results", run_id=run_id))
    except ValueError as exc:
        flash(str(exc), "error")
        return render_template("index.html"), 400


@app.get("/results/<run_id>")
def results(run_id):
    run = get_run(run_id)
    if not run:
        abort(404)
    return render_template("results.html", run=run)


@app.get("/results/<run_id>/export.xlsx")
def export_results(run_id):
    run = get_run(run_id)
    if not run:
        abort(404)
    workbook = Workbook()
    summary_sheet = workbook.active
    summary_sheet.title = "Summary"
    summary_sheet.append(["Metric", "Value"])
    summary_rows = [
        ("Review name", excel_safe(run["project_name"])),
        ("Created UTC", run["created_at"]),
        ("Total references", run["summary"]["total"]),
        ("Exact matches", run["summary"]["matched"]),
        ("Field-level mismatches", run["summary"]["mismatch"]),
        ("Missing in System A", run["summary"]["missing_a"]),
        ("Missing in System B", run["summary"]["missing_b"]),
        ("Duplicate references", run["summary"]["duplicates"]),
        ("Exact match rate", run["summary"]["match_rate"] / 100),
        ("System A source rows", run["summary"]["system_a_rows"]),
        ("System B source rows", run["summary"]["system_b_rows"]),
        ("Net amount variance", run["summary"]["amount_variance"]),
    ]
    for row in summary_rows:
        summary_sheet.append(row)
    summary_sheet["B10"].number_format = "0.0%"
    format_export_sheet(summary_sheet, [30, 32])

    sheet = workbook.create_sheet("Reconciliation Results")
    headers = [
        "Reference", "Status", "Differences", "System A Date", "System B Date",
        "System A Company", "System B Company", "System A Service", "System B Service",
        "A Adult", "B Adult", "A Child", "B Child", "A Infant", "B Infant",
        "System A Amount", "System B Amount", "Variance", "A Source Rows", "B Source Rows",
    ]
    sheet.append(headers)
    for result in run["results"]:
        left = result["system_a"] or {}
        right = result["system_b"] or {}
        sheet.append([
            excel_safe(result["reference"]), result["status_label"], ", ".join(result["differences"]) or "None",
            left.get("date", ""), right.get("date", ""),
            excel_safe(left.get("company", "")), excel_safe(right.get("company", "")),
            excel_safe(left.get("service", "")), excel_safe(right.get("service", "")),
            left.get("adult", 0), right.get("adult", 0), left.get("child", 0), right.get("child", 0),
            left.get("infant", 0), right.get("infant", 0), left.get("amount", 0), right.get("amount", 0),
            result["amount_variance"], left.get("row_count", 0), right.get("row_count", 0),
        ])
    format_export_sheet(sheet, [18, 23, 34, 16, 16, 26, 26, 24, 24] + [12] * 11)

    mapping_sheet = workbook.create_sheet("Company Mappings")
    mapping_sheet.append(["System A Label", "System B Label", "Normalized A", "Normalized B", "Result"])
    for mapping in run["mappings"]:
        mapping_sheet.append([
            excel_safe(mapping["system_a"]), excel_safe(mapping["system_b"]),
            excel_safe(mapping["system_a_canonical"]), excel_safe(mapping["system_b_canonical"]),
            "Aligned" if mapping["mapped"] else "Review required",
        ])
    format_export_sheet(mapping_sheet, [28, 28, 28, 28, 20])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="reconcileflow-demo-results.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.get("/sample-data/<system>.xlsx")
def sample_workbook(system):
    rows = SYSTEM_A if system.lower() == "a" else SYSTEM_B if system.lower() == "b" else None
    if rows is None:
        abort(404)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"System {system.upper()}"
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    format_export_sheet(sheet, [18, 15, 28, 24, 12, 12, 12, 16])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"system-{system.lower()}-demo.xlsx")


@app.get("/detailed")
def detailed_workspace():
    return render_template("detailed.html")


@app.post("/detailed/demo")
def load_detailed_demo():
    payload = reconcile_detailed(detailed_records(DETAILED_A), detailed_records(DETAILED_B))
    run_id = store_run("Synthetic detailed marine-tour review", payload)
    return redirect(url_for("detailed_results", run_id=run_id))


@app.post("/detailed/reconcile")
def upload_detailed():
    try:
        system_a_file = request.files.get("system_a")
        system_b_file = request.files.get("system_b")
        validate_file(system_a_file)
        validate_file(system_b_file)
        left = read_detailed_dataset(system_a_file.stream, system_a_file.filename)
        right = read_detailed_dataset(system_b_file.stream, system_b_file.filename)
        run_id = store_run(
            request.form.get("project_name", "").strip() or "Detailed reconciliation review",
            reconcile_detailed(left, right),
        )
        return redirect(url_for("detailed_results", run_id=run_id))
    except ValueError as exc:
        flash(str(exc), "error")
        return render_template("detailed.html"), 400


@app.get("/detailed/results/<run_id>")
def detailed_results(run_id):
    run = get_run(run_id)
    if not run:
        abort(404)
    return render_template("detailed_results.html", run=run)


@app.get("/detailed/results/<run_id>/export.xlsx")
def detailed_export(run_id):
    run = get_run(run_id)
    if not run:
        abort(404)
    workbook = Workbook()
    summary = workbook.active
    summary.title = "Summary"
    summary.append(["Metric", "Value"])
    for label, key in (
        ("Total references", "total"), ("Exact matches", "matched"), ("Mismatches", "mismatch"),
        ("Missing in System A", "missing_a"), ("Missing in System B", "missing_b"),
        ("Duplicates", "duplicates"), ("Match rate", "match_rate"),
        ("Net amount variance", "amount_variance"), ("System A pricing variance", "pricing_variance_a"),
        ("System B pricing variance", "pricing_variance_b"),
    ):
        summary.append([label, run["summary"][key]])
    format_export_sheet(summary, [32, 22])
    detail = workbook.create_sheet("Detailed Results")
    detail.append([
        "Reference", "Status", "Differences", "A Date", "B Date", "A Company", "B Company",
        "A Trip", "B Trip", "A Hotel or Pickup", "B Hotel or Pickup", "A Adult", "B Adult",
        "A Child", "B Child", "A Infant", "B Infant", "A Chargeable Pax", "B Chargeable Pax",
        "A Adult Rate", "B Adult Rate", "A Amount", "B Amount", "Amount Variance",
        "A Pricing Variance", "B Pricing Variance",
    ])
    for row in run["results"]:
        left, right = row["system_a"] or {}, row["system_b"] or {}
        detail.append([
            excel_safe(row["reference"]), row["status_label"], ", ".join(row["differences"]) or "None",
            left.get("date", ""), right.get("date", ""), excel_safe(left.get("company", "")),
            excel_safe(right.get("company", "")), excel_safe(left.get("service", "")),
            excel_safe(right.get("service", "")), excel_safe(left.get("pickup", "")),
            excel_safe(right.get("pickup", "")), left.get("adult", 0), right.get("adult", 0),
            left.get("child", 0), right.get("child", 0), left.get("infant", 0), right.get("infant", 0),
            left.get("chargeable_pax", 0), right.get("chargeable_pax", 0), left.get("adult_rate", 0),
            right.get("adult_rate", 0), left.get("amount", 0), right.get("amount", 0), row["amount_variance"],
            left.get("pricing_variance", 0), right.get("pricing_variance", 0),
        ])
    format_export_sheet(detail, [18, 22, 34] + [16, 16, 26, 26, 22, 22, 24, 24] + [13] * 15)
    reference = workbook.create_sheet("Reference Matching")
    reference.append(["System A Date", "System B Date", "Reference", "System A Amount", "System B Amount", "Variance", "Status"])
    for row in run["results"]:
        left, right = row["system_a"] or {}, row["system_b"] or {}
        reference.append([left.get("date", ""), right.get("date", ""), excel_safe(row["reference"]), left.get("amount", 0), right.get("amount", 0), row["amount_variance"], row["status_label"]])
    format_export_sheet(reference, [18, 18, 20, 18, 18, 18, 24])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="reconcileflow-detailed-demo.xlsx")


@app.get("/detailed/sample-data/<system>.xlsx")
def detailed_sample(system):
    rows = DETAILED_A if system.lower() == "a" else DETAILED_B if system.lower() == "b" else None
    if rows is None:
        abort(404)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Detailed {system.upper()}"
    sheet.append(DETAILED_HEADERS)
    for row in rows:
        sheet.append(row)
    format_export_sheet(sheet, [18, 15, 28, 24, 26, 12, 12, 12, 16, 16])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"detailed-system-{system.lower()}-demo.xlsx")


@app.get("/invoice-tracking")
def invoice_tracking():
    tab = request.args.get("tab", "overview")
    if tab not in {"overview", "companies", "analysis", "activity"}:
        tab = "overview"
    return render_template("invoice_tracking.html", data=invoice_payload(), tab=tab)


@app.get("/invoice-tracking/export.xlsx")
def invoice_tracking_export():
    data = invoice_payload()
    workbook = Workbook()
    summary = workbook.active
    summary.title = "Summary"
    summary.append(["Metric", "Value"])
    for label, key in (
        ("Companies", "companies"), ("Invoice value", "invoice"), ("Collected", "collected"),
        ("Receivable", "receivable"), ("Payable", "payable"), ("Net balance", "net"),
        ("Collection rate", "collection_rate"), ("Completed cycles", "completed"),
    ):
        summary.append([label, data["summary"][key]])
    format_export_sheet(summary, [28, 20])
    companies = workbook.create_sheet("Company Tracking")
    companies.append(["Code", "Company", "Stage", "Invoice", "Paid", "Payment", "Balance", "Direction", "Progress", "Notes"])
    for row in data["companies"]:
        companies.append([row["code"], excel_safe(row["name"]), row["stage"].title(), row["invoice"], row["paid"], row["payment"], row["balance"], row["direction"].title(), row["progress"] / 100, excel_safe(row["notes"])])
    format_export_sheet(companies, [14, 28, 16, 16, 16, 16, 16, 16, 14, 34])
    for cell in companies["I"][1:]:
        cell.number_format = "0%"
    activity = workbook.create_sheet("Activity Log")
    activity.append(["Timestamp", "Company", "Action", "Balance Before", "Balance After", "Movement"])
    for row in data["activities"]:
        activity.append([row["time"], row["company"], row["action"], row["before"], row["after"], row["after"] - row["before"]])
    format_export_sheet(activity, [22, 28, 30, 18, 18, 18])
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="reconcileflow-invoice-tracking-demo.xlsx")


@app.get("/control-center")
def control_center():
    tab = request.args.get("tab", "overview")
    if tab not in {"overview", "companies", "settlements", "no-shows", "delivery"}:
        tab = "overview"
    return render_template("control_center.html", data=control_center_payload(), tab=tab)


@app.get("/control-center/export.xlsx")
def control_center_export():
    data = control_center_payload()
    workbook = Workbook()
    summary = workbook.active
    summary.title = "Executive Summary"
    summary.append(["Metric", "Value"])
    for label, key in (
        ("Combined projects", "projects"), ("Portfolio companies", "companies"),
        ("Completion progress", "progress"), ("Receivable variance", "receivable"),
        ("Payable variance", "payable"), ("Net variance", "net"),
        ("Settlement movement", "settlement_movement"), ("No-show bookings", "no_show_bookings"),
        ("No-show value", "no_show_value"), ("Resolved exceptions", "resolved"),
        ("Open exceptions", "open"), ("Delivered companies", "delivered"),
    ):
        summary.append([label, data["summary"][key]])
    format_export_sheet(summary, [30, 22])

    projects = workbook.create_sheet("Projects")
    projects.append(["Project", "Period", "Progress", "Companies", "Open", "Receivable", "Payable"])
    for row in data["projects"]:
        projects.append([row["name"], row["period"], row["progress"] / 100, row["companies"], row["open"], row["receivable"], row["payable"]])
    format_export_sheet(projects, [24, 16, 14, 14, 12, 18, 18])
    for cell in projects["C"][1:]:
        cell.number_format = "0%"

    links = workbook.create_sheet("Unified Companies")
    links.append(["Unified Company", "System A Labels", "System B Labels", "Projects", "Aliases", "Confidence", "Status"])
    for row in data["company_links"]:
        links.append([excel_safe(row["canonical"]), excel_safe(row["system_a"]), excel_safe(row["system_b"]), row["projects"], row["aliases"], row["confidence"] / 100, row["status"].title()])
    format_export_sheet(links, [28, 38, 38, 12, 12, 14, 16])
    for cell in links["F"][1:]:
        cell.number_format = "0%"

    ledger = workbook.create_sheet("Settlement Ledger")
    ledger.append(["Date", "Time", "Project", "Reference", "Company", "Action", "Before", "Movement", "After", "Type"])
    for row in data["settlements"]:
        ledger.append([row["date"], row["time"], row["project"], row["reference"], excel_safe(row["company"]), row["action"], row["before"], row["movement"], row["after"], row["status"].title()])
    format_export_sheet(ledger, [16, 12, 24, 16, 28, 30, 16, 16, 16, 16])

    no_shows = workbook.create_sheet("No Shows")
    no_shows.append(["Reference", "Date", "Company", "Detected Shape", "Adult", "Child", "Infant", "Value", "Resolution", "Status"])
    for row in data["no_shows"]:
        no_shows.append([row["reference"], row["date"], excel_safe(row["company"]), row["shape"], row["adult"], row["child"], row["infant"], row["value"], row["resolution"].title(), row["status"].title()])
    format_export_sheet(no_shows, [16, 16, 28, 32, 12, 12, 12, 16, 16, 16])

    deliveries = workbook.create_sheet("Delivery Control")
    deliveries.append(["Company", "Project", "Bookings", "Approved Invoice", "Delivered On", "Status"])
    for row in data["deliveries"]:
        deliveries.append([excel_safe(row["company"]), row["project"], row["bookings"], row["invoice"], row["delivered_on"], row["status"].title()])
    format_export_sheet(deliveries, [28, 24, 14, 20, 16, 16])

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="reconcileflow-operations-control-demo.xlsx")


@app.get("/report-workshop")
def report_workshop():
    return render_template(
        "report_workshop.html",
        data=invoice_payload(),
        report_date=datetime.now().date().isoformat(),
    )


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "ReconcileFlow"})


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", title="Request could not be processed", message=getattr(error, "description", "Check the submitted data and try again.")), 400


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", title="Page not found", message="The requested demo result is unavailable or has expired."), 404


@app.errorhandler(413)
def too_large(_error):
    return render_template("error.html", title="File is too large", message="The public demo accepts files up to 5 MB."), 413


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "8000")), debug=False)
