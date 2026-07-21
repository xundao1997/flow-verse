# FlowVerse Architecture Baseline

## State

**CONFIRMED — SERVICE DIRECTORIES, NATIVE LOCAL ENTRY AND YUNXIAO CI TEMPLATE IMPLEMENTED; BUSINESS CONTRACTS DEFERRED**

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
| Users, traffic, and concurrency | MVP has one default user and one administrator; one user-level paid slot; one business step per task; up to three models within a step | FV1-PRODUCT-DESIGN | PRD v1.1 | PRD 7.9 and 3.10 | Confirmed |
| Data volume and growth | One real novel is the validation unit; default initial scope is a 20-chapter outline plus 3 chapters; file and history growth bounds require engineering confirmation | FV1-ARCH-BASELINE | PRD v1.1 | PRD 7.1 and UIUX package; no capacity measurements | Proposed |
| Team size and expertise | TBD — do not infer | TBD | TBD | None | Unknown |
| Timeline and phase roadmap | MVP must reach two consecutive valid real Cycles and expose a Cycle 3 entry | FV1-PRODUCT-DESIGN | PRD v1.1 | PRD 7.4 | Confirmed |
| Domain complexity and real-time needs | Long-running AI/file processing, queue/status updates, immutable formal records, revision conflicts, and atomic release-to-Cycle transition | FV1-PRODUCT-DESIGN | PRD v1.1 | PRD 3.8-3.18 and 7.11 | Confirmed |
| Compliance, privacy, and retention | Provider policy per execution; screenshots excluded from models; task data 7 days after deletion, backups 30 days, non-content security/admin audit metadata 180 days | FV1-PRODUCT-DESIGN | PRD v1.1 | PRD 3.16, 7.9, and 8.8 | Confirmed product target; implementation Unknown |
| Budget and deployment constraints | TBD — do not infer | TBD | TBD | None | Unknown |
| Availability and consistency needs | Internal MVP 99% over validation period; RTO 4h; RPO permits loss of at most 24h of unconfirmed drafts; confirmed formal data survives restart; release confirmation + Cycle creation is atomic | FV1-PRODUCT-DESIGN | PRD v1.1 | PRD 7.9 and 7.11 | Confirmed product target; topology Unknown |
| Bootstrap code/runtime topology | Separate Web, API and Worker code services; native local processes; independently supplied PostgreSQL is the only stateful bootstrap dependency; no direct API/Worker source imports | FV1-ARCH-BASELINE / FV1-LOCAL-RUNTIME / FV1-DIAGNOSTIC-BOOTSTRAP / FV1-LOCAL-TEST-DEPLOY | Service-directory, native-local, diagnostic and local deployment decisions 2026-07-15/16/20/21 | User instructions; ADR-0002, ADR-0004, ADR-0005 and ADR-0006; `services/*`; `scripts/start-local.ps1`; `deploy/local/start.ps1` | Confirmed target and repository conformance for all three native services; PostgreSQL-connected run Unverified |
| Delivery control plane | One local native test deployment wrapper; no current CI/CD control plane, remote environment or production orchestrator | FV1-LOCAL-TEST-DEPLOY | Local-test-only replacement decision 2026-07-21 | User instruction; ADR-0006; `deploy/local/` | Local target and repository conformance Confirmed; remote/production target Unknown |

## Confirmed Product Invariants for Architecture Design

- Candidate and formal state are separate; formal records, attempts, corrections, and replacements are immutable and traceable.
- Actual-release confirmation and Cycle creation are one atomic business action; one task has at most one active Cycle.
- One user has one paid AI slot, shared by model-dependent Bot and business executions; deterministic entry remains independent.
- Task, content/reference, execution/attempt, version, release/Cycle, feedback/analysis/decision, policy/configuration, identity/authorization, and audit ownership must be singular and explicitly assigned by the Proposed architecture.
- Provider/model/config/policy/input versions and actual cost are fixed in each execution record; screenshots never enter model input.
- Administrator operations cannot invoke user formal confirmations or bypass compliance.
- Read-only Agent execution trace is allowed; arbitrary wiring, custom DAG persistence, and a general Workflow Builder are forbidden.
- These invariants constrain the future architecture but do not pre-authorize module boundaries, APIs, schemas, queues, caches, databases, services, or deployment topology.

## Module Registry

| Scope ID | Package revision | Module ID | Target capability / non-goals | Owner | Target data/state and invariants | Target public entry points | Allowed / forbidden dependencies | Target evidence / ADR | Target status | Implementation evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FV1-ARCH-BASELINE | 2026-07-15 | identity_access | Identity/authorization boundary declaration; no auth behavior in bootstrap | API service | No bootstrap business data | `flowverse_api.modules.identity_access.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/identity_access/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | task_lifecycle | Task lifecycle boundary declaration; no task behavior | API service | No bootstrap business data | `flowverse_api.modules.task_lifecycle.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/task_lifecycle/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | creative_reference | Reference boundary declaration; no file adapter | API service | No bootstrap business data | `flowverse_api.modules.creative_reference.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/creative_reference/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | creative_content | Content boundary declaration; no content behavior | API service | No bootstrap business data | `flowverse_api.modules.creative_content.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/creative_content/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | review_compliance | Review/compliance boundary declaration; no policy engine | API service | No bootstrap business data | `flowverse_api.modules.review_compliance.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/review_compliance/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | ai_execution | AI execution boundary declaration and non-business Worker check; no queue/provider/job handler | Worker service | No bootstrap business data | `flowverse_worker.modules.ai_execution.public`; `python -m flowverse_worker --check` | No API source imports | ADR-0002 | Confirmed | `services/worker/src/flowverse_worker/modules/ai_execution/`; Worker tests; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | release_cycle | Release/Cycle boundary declaration; no business transition | API service | No bootstrap business data | `flowverse_api.modules.release_cycle.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/release_cycle/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | feedback_decision | Feedback/decision boundary declaration; no analysis or decision behavior | API service | No bootstrap business data | `flowverse_api.modules.feedback_decision.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/feedback_decision/`; architecture check | Confirmed |
| FV1-ARCH-BASELINE | 2026-07-15 | governance_ops | Governance/operations boundary declaration; no admin behavior | API service | No bootstrap business data | `flowverse_api.modules.governance_ops.public` | No Worker source imports | ADR-0002 | Confirmed | `services/api/src/flowverse_api/modules/governance_ops/`; architecture check | Confirmed |

## Dependency and Contract Registry

| Scope ID | Package revision | Consumer | Provider | Target public contract | Sync/async | Target failure/recovery and compatibility | Target evidence / ADR | Target status | Implementation/test evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|---|
| FV1-DIAGNOSTIC-BOOTSTRAP | 2026-07-20 | Web service | API service | Public `GET /api/v1/system/chain`; schema reports API and Worker `status` plus reason | Sync HTTP | 200 means the full chain is ready; 503 is a truthful degraded result; other status/invalid schema is an explicit Web error; one request at a time and no polling | ADR-0005 | Confirmed | API contract tests; Web parser tests; production build | Confirmed |
| FV1-BOOTSTRAP | 2026-07-15 | API service | PostgreSQL | Bounded `SELECT 1` readiness probe | Async driver call | Finite timeout; unavailable returns readiness 503; no automatic retry | ADR-0002 | Confirmed | API health tests and local degraded startup | Confirmed |
| FV1-DIAGNOSTIC-BOOTSTRAP | 2026-07-20 | Worker service | PostgreSQL | Bounded `SELECT 1` status probe exposed only through `GET /internal/v1/system/status` | Async driver call | Two-second default timeout; unavailable returns 503 with classified reason; no automatic retry | ADR-0005 | Confirmed | Worker status and failure tests | Confirmed |
| FV1-DIAGNOSTIC-BOOTSTRAP | 2026-07-20 | API service | Worker service | Internal `GET /internal/v1/system/status` | Sync HTTP | Two-second timeout, zero retries, propagated request ID; 200/503 schema is validated and all other results degrade the public chain | ADR-0005 | Confirmed | API Worker-client and chain tests | Confirmed |

## External Adapter Registry

| Scope ID | Package revision | Adapter / owner | External system | Target deadline/cancel/retry/idempotency | Data classification | Target evidence / ADR | Target status | Implementation/test evidence | Conformance status |
|---|---|---|---|---|---|---|---|---|---|
| FV1-LOCAL-TEST-DEPLOY | 2026-07-21 | Local deployment adapter / platform owner | Native Web, API and Worker launchers | `deploy/local/start.ps1` defaults to `all` and delegates every supported mode to the single `scripts/start-local.ps1` owner; no Docker/cloud path | Process environment and temporary local logs; no credential storage | ADR-0006 | Confirmed target | Local wrapper source, preflight and native chain smoke | Confirmed |

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
