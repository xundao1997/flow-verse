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
| FV1-PRODUCT-DESIGN | MVP product availability during real validation | Required | Successful usable service time over the approved validation period; exact monitoring sampling remains to be approved | 99% internal MVP target; not a commercial SLA | Exhaustion response/rollout policy TBD | Pre-release | PRD v1.1 section 7.9 | Confirmed | Delivery/operations owner TBD |
| FV1-PRODUCT-DESIGN | Work-home deterministic entry during Bot dependency failure | Required | Continue work, pending, and task list remain usable within the ordinary-page target during Bot wait/failure/policy block | Required for every exercised failure scenario | Bot failure may degrade only the Bot region; no fake success | Implementation | PRD v1.1 sections 7.5 and 7.9 | Confirmed | Product/application owner TBD |

## Recovery Target Registry

RTO/RPO rows are keyed by recoverable data set or data class, not by a stateless request flow.

| Scope ID | Data set / class | Applicability | RTO | RPO | Backup/restore scope | Gate stage | Target evidence | Target status | Verification status | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| FV1-PRODUCT-DESIGN | Confirmed formal content, releases, feedback, analyses, decisions, configuration associations, and audit evidence | Required | 4 hours | No confirmed formal record may be lost; exact backup frequency must satisfy this and remains to be designed | Persistent formal business data and required audit/configuration references | Pre-release | PRD v1.1 sections 7.9 and 7.11 | Confirmed product target | NotYetTested | Data/operations owner TBD |
| FV1-PRODUCT-DESIGN | Unconfirmed drafts and partial execution results | Required | 4 hours | At most 24 hours of unconfirmed drafts may be lost | Saved drafts and persisted partial results; client-only unsaved keystrokes excluded | Pre-release | PRD v1.1 section 7.9 | Confirmed | NotYetTested | Data/operations owner TBD |

## Failure-Control Registry

Create separate rows when controls have different applicability or gates.

| Scope ID | Boundary / operation | Control type | Applicability | Gate stage | Confirmed requirement / configuration | Target evidence | Target status | Verification status | Owner |
|---|---|---|---|---|---|---|---|---|---|
| FV1-PRODUCT-DESIGN | Actual external release confirmation and Cycle creation | Idempotency / atomicity | Required | Implementation | Create both with exact immutable bindings or create neither; one task has at most one active Cycle | PRD v1.1 sections 7.5 and 7.11 | Confirmed | NotYetTested | Release/Cycle owner TBD |
| FV1-PRODUCT-DESIGN | Formal confirmation commands | Idempotency / concurrency | Required | Implementation | Reject duplicate/stale confirmation, preserve user input, and return authoritative outcome; exact key scope/retention TBD in architecture | PRD v1.1 product/UIUX formal-action contract | Confirmed product semantics | NotYetTested | Owning domain TBD |
| FV1-PRODUCT-DESIGN | Paid Bot/business AI execution | Capacity / backpressure | Required | Implementation | One user-level paid slot, one business step per task, up to three models per step; queued work is visible and cancellable before start | PRD v1.1 sections 3.10 and 7.9 | Confirmed | NotYetTested | AI execution owner TBD |
| FV1-PRODUCT-DESIGN | AI execution lifecycle | Deadline / cancellation / retry | Required | Implementation | Maximum 30 minutes; preserve completed outputs and cost on timeout; retry/model switch creates a new attempt; never silently switch or multiply retry | PRD v1.1 sections 3.10 and 7.9 | Confirmed | NotYetTested | AI execution owner TBD |
| FV1-PRODUCT-DESIGN | Model/provider call | Policy / isolation | Required | Implementation | Evaluate current green/yellow/red policy and allowed data scope before each execution; screenshots never enter model input | PRD v1.1 sections 3.16 and 7.11 | Confirmed | NotYetTested | AI policy owner TBD |
| FV1-PRODUCT-DESIGN | Draft save and interrupted session | Recovery | Required | Implementation | Preserve input on save failure/offline/stale state; restore latest saved draft and partial result after browser/network/service interruption | PRD v1.1 sections 7.5 and 7.9 | Confirmed | NotYetTested | Draft owner TBD |
| FV1-PRODUCT-DESIGN | Task deletion and retained evidence | Data lifecycle | Required | Pre-release | Immediate user inaccessibility; task user data 7 days; backups 30 days; non-content security/admin audit metadata 180 days | PRD v1.1 section 7.9 | Confirmed | NotYetTested | Security/data owner TBD |
| FV1-BOOTSTRAP | API liveness and PostgreSQL readiness | Health / deadline / degradation | Required | Bootstrap | Liveness performs no downstream probe; readiness uses a finite 2-second PostgreSQL probe and returns 503 when unavailable; no probes PostgreSQL; readiness returns 503 and dependency detail reports degraded | User bootstrap approval; ADR-0002 | Confirmed | Passed for configuration/degraded paths; real PostgreSQL path Unverified | API service |
| FV1-DIAGNOSTIC-BOOTSTRAP | Worker PostgreSQL status probe | Deadline / Health | Required | Bootstrap | One bounded probe with 2 s default and 10 s configured maximum; no automatic retry; internal status returns 503 with a classified reason when unavailable; probe always closes | User diagnostic approval; ADR-0005 | Confirmed | Passed in unit tests; real PostgreSQL path Unverified | Worker service |
| FV1-DIAGNOSTIC-BOOTSTRAP | Web-to-API-to-Worker diagnostic chain | Deadline / Retry / Degradation | Required | Bootstrap | API calls Worker with a two-second timeout and zero retries; request ID propagates; full chain returns 503 with truthful per-service reasons when either PostgreSQL probe or Worker is unavailable; Web makes one cancellable request and never polls | User diagnostic approval; ADR-0005 | Confirmed | Passed for unit and native configuration-degraded paths; real PostgreSQL-ready path Unverified | API service |
| FV1-BOOTSTRAP | API/Worker source and module isolation | Isolation | Required | Bootstrap | Separate manifests, locks, namespaces and images; no direct cross-service source import; nine modules have singular code-service owners; production module graph remains acyclic | User instruction 2026-07-15; ADR-0002 | Confirmed | Passed | Architecture owner |
| FV1-LOCAL-TEST-DEPLOY | Local deployment entry delegation | Isolation / Recovery | Required | Bootstrap | One wrapper delegates to the registered native launcher without duplicating service commands; no Docker/cloud dependency; non-zero child exit propagates; launcher cleanup owns only its child processes | User local-test deployment instruction; ADR-0006 | Confirmed | Wrapper preflight and underlying native chain Passed; PostgreSQL-ready path Unverified | Platform/developer-experience owner |
| FV1-LOCAL-RUNTIME / FV1-DIAGNOSTIC-BOOTSTRAP | Native local process startup | Configuration / Health | Required | Bootstrap | Local startup uses no Docker; optional root `.env` never overwrites process values or prints values; `all` starts hidden API/Worker child processes, waits for liveness, keeps Web foreground and cleans up exact children on exit | User instructions; ADR-0004; ADR-0005; ADR-0006 | Confirmed | Preflight and native three-service configuration-degraded smoke Passed; PostgreSQL-ready path Unverified | Platform/developer-experience owner |

Control types include Deadline, Cancellation, Retry, Idempotency, Degradation, Isolation, Capacity/Backpressure, Health, Observability, and Recovery.

## Result Registry

| Scope ID | Target/control row | Build and environment | Scenario / command | Raw result and sample/window | Evidence | Verification status | Date |
|---|---|---|---|---|---|---|---|
| FV1-BOOTSTRAP | API PostgreSQL readiness probe | Local Windows; Python 3.13.14; no PostgreSQL configured | API unit command and real Uvicorn startup | 7 non-integration tests passed; `/health/live` 200; `/health/ready` 503; `/health/dependencies` 200 degraded; one execution | `services/api/tests/unit/`; local command output | Passed for configured-absent degradation; successful database path Unverified | 2026-07-15 |
| FV1-BOOTSTRAP | Worker PostgreSQL startup probe | Local Windows; Python 3.13.14; no PostgreSQL configured | Worker unit command and `python -m flowverse_worker --check` | 3 tests passed; real process emitted structured configuration failure and non-success exit; one execution | `services/worker/tests/unit/`; local command output | Passed for configuration-failure behavior; successful database path Unverified | 2026-07-15 |
| FV1-BOOTSTRAP | API/Worker source and module isolation | Repository source on Windows | `python scripts/check_architecture.py` | 2 Python code services; 9 singular module owners; 0 cross-module dependencies | `scripts/check_architecture.py`; checked-in service trees | Passed | 2026-07-15 |
| FV1-LOCAL-RUNTIME | Native local process startup | Local Windows; Python 3.13.14; root `.env` and PostgreSQL absent; Web source/lock absent | `scripts/start-local.ps1 preflight`; foreground `api` plus three health requests; `worker-check`; guarded `web` | Preflight exited 0 and reported Docker unused; API started on `127.0.0.1:8000`, liveness 200, readiness 503 and dependency detail 200 degraded; Worker emitted structured configuration failure; Web stopped on missing lockfile; one execution each | `scripts/start-local.ps1`; local command output | Passed for available and explicit-failure paths; configured PostgreSQL, runnable Web and long-running Worker remain Unverified | 2026-07-16 |
| FV1-DIAGNOSTIC-BOOTSTRAP | Native Web → API → Worker chain | Local Windows; Python 3.13.14; Node.js 24.17.0; PostgreSQL and root `.env` absent | Start three real service processes; request Web `/`, API chain and Web-proxied chain; stop exact processes | Web 200; API chain 503; Web proxy chain 503; both chain responses matched and reported API/Worker `configuration`; one execution | Service processes and HTTP response captured in local command output | Passed for reachability, proxy and truthful degradation; PostgreSQL-ready path Unverified | 2026-07-21 |
| FV1-LOCAL-TEST-DEPLOY | Local deployment wrapper | Local Windows; Python 3.13.14; Node.js 24.17.0; root `.env` absent | `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File deploy/local/start.ps1 preflight` | Exit 0; API/Worker runtimes, Web lock/source and exact Node runtime reported ready; Docker reported unused; one execution | `deploy/local/start.ps1`; local command output | Passed | 2026-07-21 |

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
