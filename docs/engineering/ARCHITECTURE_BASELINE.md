# FlowVerse Architecture Baseline

## State

**AWAITING_PACKAGE**

- This file is the single registry for target module/contract decisions and implemented conformance.
- Accepted ADRs or package decisions may Confirm a target; only source/config/test evidence may Confirm implementation conformance.
- Do not prefill modules from product nouns or proposed technologies.
- Unknown architecture facts block only affected cross-boundary work.

## Status Model

Target status values: Proposed, Confirmed, Conflict, Unknown, N/A.

Conformance status values: NotYetImplemented, Confirmed, Conflict, Unknown, N/A.

Target Confirmed means approved design intent. Conformance Confirmed means the current implementation has matching evidence. Never use an ADR alone as conformance evidence.

## Context Inputs

| Context | Confirmed value | Scope ID | Package revision | Exact evidence | Status |
|---|---|---|---|---|---|
| Users, traffic, and concurrency | TBD — do not infer | TBD | TBD | None | Unknown |
| Data volume and growth | TBD — do not infer | TBD | TBD | None | Unknown |
| Team size and expertise | TBD — do not infer | TBD | TBD | None | Unknown |
| Timeline and phase roadmap | Multi-phase; details TBD | Current request | N/A | Current user direction | Proposed |
| Domain complexity and real-time needs | TBD — do not infer | TBD | TBD | None | Unknown |
| Compliance, privacy, and retention | TBD — do not infer | TBD | TBD | None | Unknown |
| Budget and deployment constraints | TBD — do not infer | TBD | TBD | None | Unknown |
| Availability and consistency needs | TBD — do not infer | TBD | TBD | None | Unknown |

## Module Registry

| Scope ID | Package revision | Module ID | Target capability / non-goals | Owner | Target data/state and invariants | Target public entry points | Allowed / forbidden dependencies | Target evidence / ADR | Target status | Implementation evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Dependency and Contract Registry

| Scope ID | Package revision | Consumer | Provider | Target public contract | Sync/async | Target failure/recovery and compatibility | Target evidence / ADR | Target status | Implementation/test evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|---|

## External Adapter Registry

| Scope ID | Package revision | Adapter / owner | External system | Target deadline/cancel/retry/idempotency | Data classification | Target evidence / ADR | Target status | Implementation/test evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|

## Baseline Rules

- Intake approves target rows for its Scope ID/revision; pre-code rows may remain NotYetImplemented.
- A revised package moves only affected target rows to review; unaffected Confirmed target/conformance rows remain valid unless superseded.
- Business implementation requires affected target rows Confirmed; existing providers/consumers it relies on require Confirmed conformance.
- On completion, affected implementation rows require source/config/test evidence and Confirmed conformance.
- A local internal module inside an existing boundary does not need an ADR or new architecture-level row unless it changes public contract, dependency direction, data owner, or deployment/operational semantics.
- New architecture-level boundaries, changed dependency direction, moved data ownership, or changed deployment boundaries require an ADR and user approval.
- A module may depend only on Confirmed target dependencies; cross-module imports use target public entry points.
- Production dependency cycles are a failed gate and cannot be waived as ordinary technical debt.
- Update this baseline in the same change that alters target or implemented architecture facts.
