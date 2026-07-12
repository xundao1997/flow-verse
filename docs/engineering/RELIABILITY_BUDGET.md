# FlowVerse Reliability and Availability Budget

## Policy and Ownership

- High availability is a measured property, not an architecture label.
- Reliability targets and failure behavior require user or approved-package confirmation.
- Use the simplest topology that meets Confirmed targets.
- Do not infer replicas, regions, services, queues, caches, failover, health paths, or release strategy.
- This file owns availability, error, deadline/retry, idempotency, concurrency/backpressure, recovery, and failure-control targets.
- PERFORMANCE_BUDGET.md owns latency, throughput, bundle, interaction, and memory measurements; reference reliability row IDs instead of duplicating operational limits.

## State Model

Applicability values: Required, Optional, Unknown, N/A.

Target status values: Proposed, Confirmed, Conflict, Unknown, N/A.

Verification status values: NotYetTested, Passed, Failed, Unverified, N/A.

- At a due Gate stage, Applicability Unknown or a missing affected row blocks classification.
- A Required row must have target status Confirmed and verification status Passed before its due gate completes.
- Before the due gate, NotYetTested is valid and does not block unrelated earlier work.
- Optional does not block when omitted; if implemented or claimed, its target and verification must be Confirmed/Passed.
- N/A requires scope-specific evidence.

## Availability Target Registry

| Scope ID | Critical flow / dependency | Applicability | SLI and measurement | SLO / window | Error budget and exhaustion policy | Gate stage | Target evidence | Target status | Owner |
|---|---|---|---|---|---|---|---|---|---|

## Recovery Target Registry

RTO/RPO rows are keyed by recoverable data set or data class, not by a stateless request flow.

| Scope ID | Data set / class | Applicability | RTO | RPO | Backup/restore scope | Gate stage | Target evidence | Target status | Verification status | Owner |
|---|---|---|---|---|---|---|---|---|---|---|

## Failure-Control Registry

Create separate rows when controls have different applicability or gates.

| Scope ID | Boundary / operation | Control type | Applicability | Gate stage | Confirmed requirement / configuration | Target evidence | Target status | Verification status | Owner |
|---|---|---|---|---|---|---|---|---|---|

Control types include Deadline, Cancellation, Retry, Idempotency, Degradation, Isolation, Capacity/Backpressure, Health, Observability, and Recovery.

## Result Registry

| Scope ID | Target/control row | Build and environment | Scenario / command | Raw result and sample/window | Evidence | Verification status | Date |
|---|---|---|---|---|---|---|---|

Targets and budgets never prove results. Passed requires raw monitoring, test, restore, or failure-exercise evidence tied to the relevant row.

## Fixed Reliability Rules

### Deadlines and Retry

- Every remote call, background task, lock wait, and stream has a finite lifecycle.
- Retry only classified transient failures and respect cancellation, rate-limit signals, concurrency, resource budgets, finite attempts, and a finite total deadline.
- Never use a tight retry loop; Confirmed policy defines attempt limit, delay/backoff, jitter, and total elapsed limit.
- Exactly one layer owns automatic retry for a call chain; avoid SDK/client/gateway/task retry multiplication.
- Do not retry permission, validation, business rejection, deterministic failure, or non-idempotent side effects automatically.
- Side-effect retry requires Confirmed idempotency/deduplication covering key scope, concurrent duplicates, stored/replayed result, authoritative store, and retention/expiry window.

### Degradation and Isolation

- Degradation is explicit, observable, reversible, and approved for the affected capability.
- Never fake success, silently lose data, bypass authorization, or weaken integrity as degradation.
- Bound queues, pools, concurrency, backlog, cache, fan-out, and tenant/task resource use; apply Confirmed backpressure where required.
- Circuit breakers, bulkheads, read-only mode, queues, and caches are optional patterns, never AI defaults.
- Isolate a failing dependency/workload only when confirmed failure-domain and capacity evidence justify it.

### Health and Observability

- Liveness indicates whether the process itself is irrecoverably stuck; downstream failure alone must not cause restart storms.
- Readiness indicates whether the instance can safely accept traffic under its Confirmed dependency and initialization policy.
- Startup indicates whether required one-time initialization is complete before liveness/readiness enforcement.
- Health checks are lightweight, bounded, non-destructive, and do not expose secrets.
- Critical flows have correlated structured logs, metrics, and traces where applicable.
- Logs exclude secrets and unauthorized personal data; metric labels have bounded cardinality.
- Tool, sampling, retention, alerts, and ownership remain Unknown until approved.

### Data Protection and Recovery

- A backup does not prove recoverability.
- Passed recovery requires a restore drill, integrity checks, elapsed time, and measured data loss against the data-set RTO/RPO row.
- Migrations are repeatable or recoverable, bounded, observable, and compatible with the Confirmed deployment sequence.
- Destructive cleanup occurs only after compatibility and recovery gates pass.
- Backup frequency, retention, encryption, location, restore cadence, and ownership remain Unknown until approved.

### Failure Testing

- Test applicable timeout, dependency outage, rate limit, duplicate, reordering, partial success, restart, saturation, and recovery paths.
- Do not inject faults into production without explicit approval and a bounded safety plan.
- A failed required failure/recovery test is Failed; unavailable evidence is Unverified, never Passed.

## Stage Gates

- Intake: identify critical flows, recoverable data classes, dependencies, expected load, Applicability, owners, and recovery priorities.
- Implementation: Confirm affected deadline, retry owner, idempotency, degradation, isolation, capacity, health, and observability target rows.
- Pre-release: every Required due row has Confirmed target and Passed verification, including capacity, health, alerts, recovery, compatibility, and failure tests.
- Evolution: every API/schema/event/config change states mixed-version impact, release order, migration, removal conditions, and recovery evidence.

## Relationship to Performance

- Reliability owns operational safety limits and failure semantics.
- Performance measures latency, throughput, interaction, bundle, and memory while respecting those limits.
- A performance optimization cannot weaken reliability, and a reliability pattern cannot bypass a Confirmed performance budget.
