# FlowVerse Technical Debt Register

## State

**UNVERIFIED — package baseline audit not completed**

No entries yet is not evidence that the package or future implementation has no debt.

## Severity

- Critical: active security/data-integrity/contract-integrity risk, production dependency cycle, or Confirmed release-gate failure. It cannot be accepted as ordinary debt and blocks the affected release.
- High: likely major failure or cross-phase maintenance cost. Release requires resolution or a new explicit user risk decision with owner and future due point.
- Medium: bounded workaround or maintenance cost with a planned exit.
- Low: localized cleanup with limited impact.

Only the user may assign/change severity or accept release risk.

## Register

| ID | Introduced | Module / location | Type | Severity | Evidence and impact | Reason | Compensating control | Owner | Due phase | Due date | Exit criteria and verification | Status | Approval / ADR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Types include architecture, contract, data, test, reliability, performance, security, dependency, and operations.

Status values: Proposed, Accepted, Planned, InProgress, Resolved, Superseded.

Active statuses: Proposed, Accepted, Planned, InProgress.

## ID and Expiry Rules

- An active TODO/FIXME/HACK/flag/shim/dual path has a valid ID only when the register row exists, location matches, status is active, and it is not expired.
- Resolved or Superseded entries must have no active code marker or temporary path referencing them.
- A row is expired when its calendar due date has passed, or the current release/phase has reached its due phase, and exit criteria are not verified.
- An expired active row fails the affected gate until resolved or the user records a new risk decision and future due point.

## Debt Rules

- AI may create Proposed entries; only the user may Accept risk, change severity, or extend a due point.
- Debt records owner, impact, temporary control, due phase/date, removal trigger, exit criteria, and verification.
- Debt cannot waive security, data correctness, contract compatibility, production dependency cycles, or a Confirmed reliability/performance gate.
- Touching existing debt must not expand its responsibility, dependency surface, data risk, or expiry without approval.
- Imported package debt is recorded as baseline; do not rewrite unrelated areas opportunistically.
- Each product phase reviews Critical/High and due entries before release.
- Resolved requires code/test/measurement evidence; deleting the entry, test, alert, or budget is not resolution.
- AI cannot silently defer, downgrade, or permanently accept debt.
