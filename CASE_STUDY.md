# ReconcileFlow product case study

## Executive summary

ReconcileFlow began as a response to a finance operations problem: two parties can record the same marine-tour activity differently, while a spreadsheet review becomes slower and less reliable as months, companies, booking lines, and exceptions increase.

Over a three-month iterative build, the control expanded from simple amount matching into a broader operating system for reconciliation, exception resolution, settlements, company delivery, detailed pricing, invoice follow-up, and report production. This public package recreates the three main workflows and a live Operations Control Center with synthetic data, without exposing the original database or organization identities.

## My role

I approached the project as a finance and accounting operations professional using technology to solve a control problem. My contribution was to identify the business rules, define the meaning of each exception and balance, test the output against the working process, and continuously refine the workflow around real review needs.

The case study should not be positioned as a claim of senior software engineering experience. It demonstrates accounting judgment, requirements analysis, process ownership, data-quality thinking, and the practical use of Python and web technology.

## Workflow 1: standard reconciliation

The standard workspace keeps the familiar booking-level review intact. Each project contains separate source views, company-name matching, comprehensive reconciliation, company-specific differences, and analysis.

Key control decisions:

- Preserve both source labels while linking many names to one company when needed.
- Allow many-to-one and one-to-many company-name relationships.
- Compare date, company, passenger categories, and amount using a repeatable key.
- Keep missing records and duplicates visible rather than silently dropping them.
- Support row addition, editing, deletion, company-level deletion, and supplemental Excel imports.
- Keep filters and navigation position stable while moving between summaries and booking details.

## Multi-project and unified-company control

Multiple monthly or period projects can be opened as one combined working space. Companies from different projects are linked under a unified name, while edits still update their original project records.

The design includes:

- project selection without changing the standalone projects;
- cross-project company linking and unlinking;
- explicit “not present in this project” states;
- repeated source names where business reality requires them;
- combined company differences, analysis, settlements, and exports.

## Exception lifecycle and resolution

The operational workflow distinguishes unresolved differences from two meaningful resolution paths:

- **Automatically resolved:** the balance reaches zero through matching or correction.
- **Resolved by agreement:** the balance is accepted through a documented manual decision.

Resolved and unresolved bookings are counted and valued separately so that a zero balance is not confused with an undocumented override.

## Settlement and audit ledger

When a source amount is changed, the system records the prior amount, new amount, direction, date, time, project, company, and booking context. Booking deletion is also treated as a financial movement. Repeated edits remain reconcilable without double-counting the current net effect.

The ledger can be filtered by date, project, company, booking, and movement direction; totals follow the complete filtered set.

## No-show treatment

A no-show remains part of the financial record rather than being deleted. The design supports several operational forms:

- a booking present in one source only;
- a booking present in both sources with a zero value on one side;
- a partial no-show affecting only selected adults, children, or infants;
- a no-show attached to only part of a repeated booking reference.

No-show booking count, adult/child/infant quantities, and value feed the company and project analysis.

## Workflow 2: detailed reconciliation

Detailed reconciliation is a separate mode so the stable standard workflow is not disrupted. It adds:

- booking reference;
- marine-tour trip type and trip-name mapping;
- hotel or pickup location;
- transfer presence, inferred from the pickup field;
- adult rate;
- chargeable passengers: adults plus half the children;
- zero infant cost;
- calculated amount and pricing variance;
- automatic rate derivation when amount is present;
- automatic amount derivation when rate is present;
- an independent reference-number reconciliation table with separate dates for both sources.

This makes it possible to distinguish a booking-value difference from a pricing-rule, passenger-mix, trip, or pickup difference.

## Company review, delivery, and approved statements

Company work progresses through clear operational states: not started, under review, reconciled, report sent, response received, and closed. Completed companies can move below the active review queue.

A separate delivery control identifies companies whose reviewed booking set has been handed over. The final statement is based on the corrected primary-source bookings and includes signature and stamp space, without introducing tax assumptions.

## Workflow 3: invoice tracking

Invoice Tracking is intentionally independent from booking reconciliation. Company names and opening invoice values are managed centrally, while day-to-day follow-up records payment and workflow progress.

The balance formula is:

`Invoice value - recorded paid amount - additional payment`

A positive balance is receivable, a negative balance is payable, and zero is settled. The workspace includes stage progress, collection rate, open balance ranking, financial direction analysis, filters, exports, and an activity history.

## Signature feature: Report Workshop

The Report Workshop was designed to avoid rigid one-purpose PDFs. Before printing, the reviewer can decide what belongs in the document:

- title and subtitle;
- sender and recipient;
- preparer;
- report date;
- notes;
- each organization logo independently;
- summary metrics;
- table columns.

Defaults are ready for immediate use, while the latest choices persist until changed. Reports inherit the active filter's complete dataset rather than only the currently paginated rows, and the printed document does not expose filter-interface language.

## Performance and reliability decisions

- Pagination and bounded imports protect the interface from very large tables.
- Filter state and navigation state are retained across drill-down and return workflows.
- Asynchronous actions prevent unnecessary full-page reloads in the operational interface.
- Incremental recalculation limits work to affected records where practical.
- Financial movements and destructive actions are treated as auditable events.
- Synthetic public data is separated from operational databases and backups.

## Public demonstration boundary

The interactive portfolio includes the three main paths, the Report Workshop, and synthetic control views for combined projects, unified companies, settlements, no-shows, resolution states, and company delivery. It demonstrates the product's breadth without copying the operational database or confidential organization identities. The public demo does not claim multi-user production readiness and intentionally omits client branding, authentication, and production data.
