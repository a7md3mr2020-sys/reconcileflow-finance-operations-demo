# Reconciliation logic

## Input contract

Each source requires eight columns: `Reference`, `Date`, `Company`, `Service`, `Adult`, `Child`, `Infant`, and `Amount`. Common English header variations are accepted. Empty rows are ignored; partially populated rows are validated and reported with their row number.

## Normalization

- Text is normalized with Unicode NFKC, uppercase conversion, punctuation removal, and whitespace collapse.
- Dates accept ISO and common day-first formats, plus Excel serial dates.
- Passenger and amount fields must be finite non-negative numbers; blank numeric cells become zero.
- Original company and service labels remain in the result for traceability.
- A small explicit alias dictionary demonstrates controlled company-name mapping.

## Matching and aggregation

`Reference` is the matching key. Multiple rows with the same reference in one source are aggregated for passenger counts and amount. The reference is then classified as a duplicate, keeping the quality issue visible.

## Outcome definitions

| Outcome | Definition |
|---|---|
| Matched | Present once in both systems, with all compared fields equal. |
| Mismatch | Present once in both systems, but one or more compared fields differ. |
| Missing in System A | Present only in System B. |
| Missing in System B | Present only in System A. |
| Duplicate detected | Repeated in either source, regardless of any additional differences. |

The amount is different when the absolute variance is greater than or equal to `0.01`.

## KPI definitions

- **Total references:** unique references found across both sources.
- **Exact matches:** references classified as Matched.
- **Match rate:** exact matches divided by total references.
- **Missing records:** Missing in System A plus Missing in System B.
- **Amount variance:** sum of System A amount minus System B amount across every reference.

## Demonstration limitations

The matching key, fields, and classifications reflect the bundled marine-tour scenario. Production use would require configurable matching rules, authorization, an audit trail, managed storage, background processing, data-retention controls, and formal user acceptance testing.
