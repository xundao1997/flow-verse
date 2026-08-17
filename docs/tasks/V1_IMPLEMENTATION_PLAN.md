# FlowVerse V1 Implementation Plan

## Status

- Product/design scope `FV1-PRODUCT-DESIGN` is approved from PRD v1.1 and the FlowVerse Phase 1 UIUX MVP package.
- The user's 2026-08-12 product-roadmap direction names cumulative V1.0 novel creation, V1.1 AI content analysis/operations review, and V1.2 feedback-driven AI creation/closed-loop effect releases. The exact partition in this plan is `IN_REVIEW` under `FV1-ROADMAP-REVIEW`; the external PRD remains unchanged and authoritative for retained behavior and the final V1.2 result until the whole synchronized change set receives final approval.
- Architecture and non-business bootstrap scopes are approved through `FV1-SERVER-DATA-EXTENSIONS`. Web/API/Worker source, locks, diagnostic contracts, quality gate, native local-test entry and server PostgreSQL/Redis/MinIO configuration are implemented; PostgreSQL packages pgvector and TimescaleDB OSS without creating schemas. One target-server middleware image-build and three-container health smoke passed after the recorded compatibility corrections, and the PostgreSQL-ready native application chain passed locally on 2026-07-30. Extension SQL availability, sustained operation and recovery remain external gates; CI/CD and application production deployment are Unknown.
- No business implementation may begin until the relevant architecture targets, technology versions, commands, file scope, acceptance mapping, and due reliability/performance gates satisfy `../engineering/AI_CODING_WORKFLOW.md`.
- V1.0 is the first implemented product release. Direction-document provenance creates no migration or legacy compatibility work.

## Cumulative Product Release Train

| Release | Entry and outcome | Implementation slices | Required release gate |
|---|---|---|---|
| V1.0 — 小说场景 | New task → confirmed `CreationBaseline` → governed initial AI candidates → Review/memory confirmation → first immutable formal novel snapshot and content export | Identity/shell; task and creation baseline; references; settings/characters/outline/initial chapters; initial creation execution; Review/memory/versions; due governance/export/delete/recovery | V1.0 first-due assertions and horizontal gates, including mandatory `DataSafetyGate`; `AvailabilityGate` only when separately made applicable; no release/Cycle or unapproved HA claim |
| V1.1 — AI 内容分析与运营复盘 | V1.0 formal snapshot → confirmed `OperationValidationBaseline` → packaging/release plan → one real manual release → feedback → AI analysis candidate → formal analysis → formal human decision | V1.0 regression; operation-baseline extension; packaging and release plan; actual release/Cycle; feedback/correction; analysis; continue observation/formal decision; due governance/review export/recovery | One real valid Cycle plus V1.0 cumulative regression and affected horizontal-gate requalification. “Continue observing” cannot satisfy completion |
| V1.2 — AI 内容创作与运营闭环效果 | Current eligible formal decision → bounded next-round plan/input → AI content or packaging candidates → human-confirmed actual change → adjacent valid release/review → comparison/value result/following Cycle N+2 | V1.0/V1.1 regression; decision-driven execution; next-round content/packaging; adjacent release; Cycle N/N+1 comparison; value collection/reporting; complete governance/export/recovery | All AC-01-35, all PRD 7.5/7.6, the first adjacent pair of real valid Cycles, following Cycle N+2 path, and all affected horizontal-gate evidence |
| V2.0 — 金融研究 | Stocks/funds/futures analysis and review | Architecture preparation only until a separate approved financial PRD, compliance/data contract, acceptance, and file-level plan exists | No V1 AC may be reused to claim V2 product acceptance |

Every later V1 release must preserve readable formal history and pass every earlier due contract. Database/API/schema migrations, when later approved, require explicit upgrade and rollback evidence; no release may depend on a future release to keep its own formal content readable, exportable, or recoverable.

### Release-train execution order

Phase numbers below group cohesive work; they are not a command to finish V1.2 feature work before V1.0 horizontal controls. Phases 5 and 8 are cross-release lanes, and Phase 9 is three separate release gates:

| Lane | Required before that release |
|---|---|
| H0 / V1.0 | Phases 3–4 + only the V1.0 workloads in Phase 5 + the AC-32A/33A/34A and other V1.0 controls in Phase 8 + the V1.0 part of Phase 9 |
| H1 / V1.1 | H0 regression + Phase 6 + the V1.1 additions in Phases 5/8 + the V1.1 part of Phase 9 |
| H2 / V1.2 | H0/H1 regression + Phase 7 + the V1.2 additions in Phases 5/8 + the V1.2 part of Phase 9 |

No release may defer its due export, deletion, recovery, Prompt-governance, reliability, performance, accessibility, security, or real-evidence gate merely because that work appears in a later-numbered cross-release section.

### Gate split: data safety versus production availability

Status: `IN_REVIEW / Proposed`.

- `DataSafetyGate` is mandatory at H0 and cumulative at H1/H2. It covers PostgreSQL-authoritative formal records, object/reference/export consistency, atomic and idempotent formal writes, backup/PITR, restore, readable history, deletion non-resurrection, and conservative degradation. Redis remains non-authoritative and must not change formal truth when unavailable or lost.
- `AvailabilityGate` is a separate deployment/operations gate. It becomes applicable only after an explicit human decision fixes the target environment, measurement window, fault domain, monitoring, capacity, budget, and owner. The Confirmed target remains `99%` during internal MVP validation and is not a commercial SLA.
- The `99.9%` monthly target, multi-AZ quorum/fencing, N-1 capacity, and replica counts remain `Proposed`; they cannot block H0 merely by appearing in a target architecture. If they are separately selected for V1.0 production, their evidence is required before that production availability claim. A recovery result cannot substitute for availability evidence, and a non-applicable availability gate cannot waive data safety.

### Per-release physical capability allowlist

This execution allowlist mirrors `../uiux/RELEASE_CAPABILITY_MATRIX.md`. Each release manifest expands it to exact route, actor, viewport, state, dialog/action, and negative deep-link assertion; source files must not introduce a route/action merely because a shared component exists.

| Gate | Implementable physical scope | Required negative scope |
|---|---|---|
| H0 / V1.0 | AUTH; P01; `CreationBaseline` Stage 0; P02; initial-creation P03; V1.0 Bot/Agent trace/pending/settings/activity; V1.0-scoped A01-A08 including A05; D01, D02 content, D03, D10, D11 content package | No P04/P05, V1.1 operation fields/workloads, D02 packaging, D04-D09, D12, next-round/comparison/value, or V2 route/action |
| H1 / V1.1 | H0 regression plus `OperationValidationBaseline` Stage 0, P03 packaging handoff, P04, P05 analysis/decision, V1.1 A01-A08 extensions, D02 packaging, D04-D09, D11 review package, D12 `cycleTimeReconciliation` | No P05 next-round/comparison/value, decision-driven creation, D12 `twoCycleSurvey`, or V2 route/action |
| H2 / V1.2 | H0/H1 regression plus P03 decision-driven creation, P05 next-round/comparison/value/following Cycle N+2, V1.2 A01-A08 extensions, D11 complete-lineage package, D12 `twoCycleSurvey` | No V2 financial route, object, data, or action |

Not-introduced and unknown/stale capabilities are absent from ordinary navigation, Bot targets, pending/activity and mutation; authorized historical objects remain readable only with a truthful freshness state, and no rejected deep link creates partial business state.

The same release manifest must consume the numbered data/API catalog rather than only UI routes. Its business allowlist carries the exact release `T`/`PUB` sets and business internal `INT-001–INT-010`: H0 permits the exact H0 sets, while H1/H2 add their exact `T`/`PUB` deltas and only the approved internal family/schema/capability overlays. H0 allows only `AI_EXECUTION`, `DOCUMENT_PROCESSING`, `EXPORT_GENERATION`, and narrowly scoped `MAINTENANCE`; maintenance permits only `DELETION_RECONCILIATION` and `RECOVERY_CHECKPOINT_BUILD` with their typed targets. Unknown or not-yet-due job types/subtypes, Prompt families, schema versions, and capabilities fail at registration, claim, and report.

An independent operational allowlist carries exactly five H0 rows: `OPS-API-001..003` for API `GET /health/live`, `GET /health/ready`, and `GET /health/dependencies`, plus `OPS-WORKER-001..002` for private Worker `GET /health/live` and `GET /health/ready`. They are outside both the 107-row business Public catalog and the 10-row business Internal catalog, cannot unlock any product route/action/command, and are not evidence of product readiness, `DataSafetyGate`, or `AvailabilityGate`. Production H0 retires the complete ADR-0005 diagnostic chain as one unit: the Web Check page is absent from the product router/build, public `GET /api/v1/system/chain` and `GET /internal/v1/system/status` return `404/410`, and a negative dependency test proves the API no longer calls Worker status. ADR-0005 may retain all three only in an explicitly isolated non-production diagnostic profile; the five approved `OPS-*` health routes remain available as operational exceptions without becoming business capabilities.

Worker/JIT/DeliveryStore failure is interpreted by the registered job type, not by one generic execution screen: AI is shown on its owning execution resource, document processing on the P03 reference-processing state, and export generation on the D11 export-request state. New document processing and new or repeated export generation fail closed; PostgreSQL-backed formal content and request metadata remain readable. An already generated authorized package remains previewable/downloadable only while ObjectStore currently proves the requested version, integrity, authorization, and readable bytes. Mobile may inspect status and such a currently proven existing D11 package, but may not start or retry AI, document processing, export generation, or recovery mutations.

### H0 benchmark input contract

The external PRD already fixes the following H0 workload inputs and they must be present in the benchmark fixtures: no more than 20 files per task, 10 MB per file, 500,000 characters per file, 2,000,000 characters per task, and 300 pages per text PDF. The representative novel fixture also starts from the product default of a 20-chapter outline plus the first 3 chapters; because the user may adjust this in the Creation Baseline, it is not a hard capacity ceiling.

These are inputs, not measured results. Before the H0 performance gate can be classified, a human must still approve lab environment/resources, network, cold/warm state, concurrency and queue profile, sample count/noise, executable commands, and per-test warning/failure thresholds consistent with any already Confirmed product-level targets. Until then the performance gate is `Unverified`; the team must not pre-emptively introduce Redis business state, read replicas, a broker, or another datastore to compensate for an unmeasured result.

### User decision register for release execution

| Decision | Minimum decision record | State until recorded |
|---|---|---|
| `UD-PG-01` PostgreSQL | Production/validation writer and fault-domain boundary, backup/PITR mechanism, formal-record RPO implementation and operations owner | `DataSafetyGate` blocked; diagnostic health is insufficient |
| `UD-OBJ-01` object storage | Business account/bucket, TLS/encryption, isolation, lifecycle/version/delete, backup/restore, and PostgreSQL-object recovery checkpoint | Reference-dependent formalization, export and recovery blocked; middleware health is insufficient |
| `UD-REC-01` recovery | Recoverable data-set inventory, RTO/RPO exercise, restore owner, deletion-ledger or equivalent non-resurrection mechanism and reconciliation evidence | H0 recovery evidence `Unverified` |
| `UD-DEG-01` degradation | Per PostgreSQL/object/provider/queue failure: permitted read-only and draft behavior, blocked formal writes/AI actions, freshness disclosure, bounded retry, and user recovery action | Affected mutation and AI execution fail closed |
| `UD-PERF-01` performance | H0 environment, concurrency, samples, commands, noise and per-test thresholds using the fixed input fixture | H0 performance evidence `Unverified` |
| `UD-AVL-01` availability | Internal-MVP-only 99% validation or a separately applicable production `AvailabilityGate`; if the latter, fault domain, window, capacity, budget, monitoring and owner | No 99.9% or production-HA claim; `DataSafetyGate` remains applicable |

## Version-Level Traceability Gate

Before business implementation begins for any release, create an approved traceability artifact whose every row names:

- authoritative PRD or UIUX source and exact requirement/scenario ID;
- repository AC or child assertion, first-due release, and cumulative regression releases;
- physical allowlist or required negative-capability assertion for the release;
- user-visible result and deterministic/AI-candidate/human-confirmation boundary;
- module and singular data owner, public contract and dependency direction;
- exact implementation and test files after their paths receive explicit approval;
- functional, UIUX/accessibility, security/privacy, reliability, performance, recovery, and real-evidence gate status;
- `DataSafetyGate` evidence, `AvailabilityGate` applicability/decision ref, H0 benchmark fixture/profile when due, and all applicable user-decision refs;
- Passed, Failed, N/A, or Unverified with exact evidence and the recovery/rollback path.

A release marks each due child assertion independently. A split top-level parent remains `Partially qualified / Unverified`, never Passed, until all children in its complete V1.2 scope pass. A not-yet-due child is `Deferred to V1.x`, not Passed or N/A. V1.2 must close the full PRD 7.5/7.6 and UIUX 1-130 mapping; the versioned UIUX scenario split remains a separate approval gate.

## Phase 1: Architecture and Reliability Review — Current

Deliver a Proposed, reviewable architecture without business code:

- Confirm team expertise, delivery timeline, deployment/budget constraints, data/document/history scale, compliance owner, operational owner, and environment.
- Define cohesive target modules, non-goals, singular data/invariant owners, public contracts, and directed dependencies.
- Define candidate/formal/version ownership; atomic actual-release-to-Cycle boundary; AI execution/attempt/policy/cost boundary; auth/admin/audit boundary; file/reference boundary; deletion/export/recovery boundary.
- Select the simplest viable target stack and modular-monolith/process topology; compare queue, cache, object storage, database, streaming/status, and provider-adapter options.
- Record deadlines, retry ownership, idempotency, cancellation, concurrency/backpressure, degradation, observability, RTO/RPO, backup/restore, retention, and failure tests.
- Draft ADRs for every selected framework, database, queue, persistent cache, provider abstraction, auth strategy, public/data/deployment boundary, and recovery strategy.
- Populate `../engineering/ARCHITECTURE_BASELINE.md`, `TECH_STACK.md`, `RELIABILITY_BUDGET.md`, `PERFORMANCE_BUDGET.md`, the decision log, and debt register. Only the user may Accept ADRs or approve target rows.

## Phase 2: Conditional Engineering Bootstrap

### Approved service-directory slice — 2026-07-15

- Outcome: independent `services/web`, `services/api`, and `services/worker` code/build boundaries; no product behavior.
- Acceptance mapping: product ACs N/A; AC-20 and AC-35 remain negative guards. No Agent builder, Prompt editor, arbitrary DAG, automated publishing or value claim is implemented.
- API-owned modules: identity/access, task lifecycle, creative reference, creative content, review/compliance, release/Cycle, feedback/decision and governance/operations.
- Worker-owned module: AI execution. API and Worker have no business contract in this slice and may not import each other's source.
- Public operational contracts: API `GET /health/live`, `GET /health/ready`, `GET /health/dependencies`; Worker `python -m flowverse_worker --check`.
- Data: API owns the empty Alembic baseline; neither service defines a business table; PostgreSQL is the only runtime data dependency.
- Affected files: `services/**`, `.env.example`, root runtime-version files, `scripts/check_architecture.py`, ADR/intake/engineering registries and this plan. The former Compose entry was later removed by ADR-0004.
- Excluded: product/UIUX sources, auth, business APIs/schemas, queue/broker/cache, object-storage adapter, AI provider and production runtime/CD.
- Verification: service-specific Ruff/Pyright/pytest; Alembic head; architecture check; real degraded API startup; Worker configuration-failure process. Docker/PostgreSQL-connected and Web checks remain Unverified.
- Recovery: reverse only the in-repository service moves and exact documentation changes; preserve user work and volumes; no destructive Git operation.

### Superseded cloud-delivery slice — 2026-07-15

- The repository once contained a proposed cloud pipeline and host-deployment adapter. The user superseded that direction on 2026-07-21 through ADR-0006, and its implementation was removed.
- This slice is retained only as decision provenance. It is not a current target, command, acceptance result or compatibility obligation.
- CI/CD, registry, test-server and production deployment targets are Unknown until separately selected and approved.

### Approved native-local and root README slice — 2026-07-16

- Outcome: root `README.md` documents product scope, service/module ownership, package versions, native commands, the then-current deployment boundary and blockers; `scripts/start-local.ps1` provides native `preflight`, API, Worker-check and guarded Web entries; root Compose is removed.
- Acceptance mapping: product ACs are N/A; AC-20 and AC-35 remain negative guards. No product UI, AI behavior, automated publication or workflow builder is added.
- Owner and contracts: platform/developer-experience owns the script. It loads optional root `.env` values without printing them or overriding process-level values. Public application APIs, schemas, auth, module/data owners and ports remain unchanged.
- Affected files: root `README.md`, `.env.example`, `scripts/start-local.ps1`, removal of `compose.yaml`, ADR-0004, delivery runbook and engineering/governance/task registries.
- Excluded: service business code, new dependencies, frontend version resolution, Worker daemon behavior, PostgreSQL installation, cloud credentials/resources and executable production CD.
- Reliability/security: native processes run in the foreground; missing runtimes/source/lockfiles fail explicitly; no secret values are echoed; API health semantics and Worker exit classes remain unchanged.
- Verification: run script preflight, real API health startup, Worker configured/absent dependency path, guarded Web failure, PowerShell syntax, architecture check, credential scan and diff check.
- Performance: N/A because documentation and process-launch orchestration add no product runtime path; service performance remains separately Unverified where recorded.
- Recovery: restore only the removed Compose file if the decision is explicitly reversed, delete the new root/script/ADR files and reverse exact registry edits; do not touch PostgreSQL data or cloud resources.

### Approved deployment-diagnostic completion slice — 2026-07-20

- Outcome: a runnable Simplified-Chinese Check page calls public `GET /api/v1/system/chain`; API calls Worker internal `GET /internal/v1/system/status`; API and Worker each report their PostgreSQL probe; native `all` starts the three code services. The former production-delivery portion is superseded by ADR-0006.
- Acceptance mapping: AC-24, AC-26, AC-28, AC-29 and AC-30 apply only to this diagnostic surface and are covered by source/tests/build; all business ACs remain N/A. AC-20 and AC-35 remain negative guards.
- Owners and contracts: Web owns display/request lifecycle; API owns the public aggregate; Worker owns its internal status; each Python service owns its PostgreSQL probe. No business module or data owner changes.
- Affected files: diagnostic source/tests/config under `services/**`, `.env.example`, native and architecture scripts, ADR-0005 and affected registries/runbooks. Former cloud-delivery files are no longer part of this slice.
- Excluded: authentication, product routes, business APIs/schemas/tables, queue/broker/Redis, object storage, AI providers/jobs, production values, cloud resource creation and successful cloud execution evidence.
- Reliability/security: two-second API-to-Worker deadline, zero retries, request correlation, truthful 503 degradation, generic correlated 500 responses, no Web polling and no committed secrets.
- Release-scope boundary: this historical Check/public-chain/internal-status trio is one non-production diagnostic capability. Production H0 removes all three together and retains only the separately allowlisted five `OPS-*` health routes (three API and two private Worker routes); those health routes do not enter product navigation or prove a business release gate.
- Verification: Web lint/format/typecheck/test/build; API and Worker Ruff/Pyright/pytest; architecture checker plus self-tests; native preflight and three-service smoke; documentation consistency. PostgreSQL-ready execution remains Unverified when the required external runtime is absent.
- Performance: initial production bundle sizes are recorded in `../engineering/PERFORMANCE_BUDGET.md`; connected latency, image sizes and field metrics await their named environments.
- Recovery: terminate only launched child processes; reverse only this diagnostic slice if the approved decision is superseded; never delete PostgreSQL data.

### Approved local-test deployment replacement — 2026-07-21

- Outcome: remove the superseded cloud-delivery directory and expose `deploy/local/start.ps1` as the stable native local-test entry; the wrapper delegates to `scripts/start-local.ps1` and defaults to `all`.
- Acceptance mapping: product ACs are N/A; AC-20 and AC-35 remain negative guards. No business behavior, Agent/workflow editor or automated publication is added.
- Owner and contracts: platform/developer-experience owns the wrapper. Existing service ports, health endpoints, diagnostic contracts, module/data owners and dependencies are unchanged.
- Affected files: `deploy/local/**`, removal of the former cloud-delivery directory, ADR-0006 and affected architecture/stack/reliability/governance/task documentation.
- Excluded: Docker orchestration, CI/CD, cloud registry, test-server or production deployment, credentials, application contracts, schemas and business code.
- Reliability/security: one wrapper delegates without duplicating orchestration; child failures propagate as non-zero exits; underlying launcher cleanup remains the single process-lifecycle owner; no secret values are printed.
- Verification: execute the wrapper in `preflight` mode, run architecture checks and self-tests, scan current documentation for stale active-cloud claims, and review the diff. PostgreSQL-ready execution remains Unverified.
- Performance: N/A because the wrapper adds no application runtime path and starts the same native processes.
- Recovery: remove the wrapper and reverse only ADR-0006/current registry edits if a replacement deployment decision is explicitly approved; preserve application data and user work.

### Approved local-to-server middleware development access — 2026-07-24

- Outcome: allow the native Windows development environment to use the already deployed private PostgreSQL, Redis and MinIO endpoints through one foreground OpenSSH local-port-forward command, without exposing middleware ports publicly.
- Acceptance: require an explicit SSH host/user; bind local forwards only to `127.0.0.1`; default to non-conflicting local ports 15432/16379/19000/19001; permit port and identity-file overrides; reject duplicate ports; keep SSH host-key verification; use a 10-second connection timeout, `ExitOnForwardFailure` and bounded keepalive; propagate SSH failure; store/print no middleware credential; support a no-network `-ValidateOnly` check.
- Owner and contracts: platform/developer-experience owns the tunnel helper. The local API/Worker continue consuming only `FLOWVERSE_DATABASE_URL`; Redis/MinIO application contracts remain N/A. Server Compose, data owners and service topology are unchanged.
- Affected files: `deploy/local/start-middleware-tunnel.ps1`, local/root runbooks, the root non-secret environment example, and active intake/architecture/stack/reliability/governance/task evidence.
- Excluded: `services/**`, server Compose, public binds, firewall/security-group changes, SSH accounts/keys, password rotation/storage, Redis/MinIO business integration, TLS, CI/CD and application production deployment.
- Reliability/security: the tunnel is foreground and reversible; closing it removes every forward; no automatic retry hides failure; local and server middleware listeners remain loopback-only; live SSH authentication and reachability are operator-owned external prerequisites.
- Verification: parse the PowerShell script, run the registered no-network validation command, assert duplicate ports fail, scan for public-bind/credential drift, run architecture checks/self-tests and `git diff --check`. A real SSH session is intentionally Unverified until the operator supplies and authorizes a server endpoint.
- Performance: product loading/rendering/bundle/AI performance is N/A because the helper changes no application code. Tunnel latency and throughput are Unverified and depend on the developer network and SSH server.
- Recovery: press `Ctrl+C` to remove forwards; delete the helper and documentation/evidence rows to roll back. No server restart, migration or data-volume action is required.

### Approved server-middleware deployment slice — 2026-07-22

- Outcome: add one server-only Docker Compose project for PostgreSQL 18.4 with pgvector 0.8.5, Redis 8.8.0 and source-built MinIO `RELEASE.2025-10-15T17-29-55Z`; preserve the Docker-free native local application path.
- Acceptance: exactly three services; no committed secret values; loopback port defaults; file-secret mounts; named persistent volumes; health/restart/process/log/CPU/memory controls; explicit host disk-capacity plan; non-destructive stop/recovery instructions; pinned version evidence and ADR.
- Owner and contracts: platform/operations owns provisioning. PostgreSQL is authoritative relational storage, Redis is non-authoritative capability, and MinIO is object-storage capability. No application consumer, API, schema, extension, bucket or user contract is created.
- Affected files: `deploy/server/middleware/**`, ADR-0007, root README and affected intake/architecture/stack/reliability/performance/governance/task registries.
- Excluded: `services/**`, local launcher behavior, Elasticsearch/OpenSearch, TimescaleDB, business schema/API/auth, application credentials/connections, CI/CD, application production deployment, TLS, backup/restore, monitoring, high availability and destructive data operations.
- Verification: statically review Compose inline image recipes and one-command bootstrap, scan for secret leakage, run script syntax, architecture and diff checks; on the target server run registered Compose config/build/start/health commands. The corrected image-build and three-service-health smoke passed once on the target server; exact updated one-command rerun and local Docker execution remain Unverified.
- Recovery: `docker compose down` stops only this project and preserves named volumes. Never use `down -v` as routine rollback; any data migration/removal requires a separately approved plan and superseding ADR.

### Approved PostgreSQL extension bundle — 2026-07-22

- Outcome: retain the three-container middleware topology while packaging pgvector 0.8.5 and TimescaleDB 2.28.3 OSS in PostgreSQL 18.4 for future simple RAG and stock time-series work.
- Acceptance: exact extension versions compiled in an isolated stage over the existing Debian PostgreSQL runtime; TimescaleDB shared preload with bounded workers and telemetry disabled; no automatic initialization script, `CREATE EXTENSION`, table, hypertable, vector index or policy; extension-availability query documented; existing secrets, ports, volumes and service count unchanged.
- Owner and contracts: platform owns extension binaries and PostgreSQL process configuration. Future Alembic migrations own activation and all vector/time-series schemas. PostgreSQL remains the single relational authority; no new dependency edge or data owner is created.
- Affected files: PostgreSQL middleware inline Compose recipe/non-secret settings/runbook/bootstrap, ADR-0008 and affected intake/architecture/stack/reliability/performance/governance/task/root documentation.
- Excluded: `services/**`, migration files, embedding provider/model/dimension, RAG ingestion/query APIs, market-data tables/hypertables, retention/compression policies, pgvectorscale, Elasticsearch/OpenSearch, a separate TimescaleDB service and any data-volume mutation.
- Verification: statically confirm exact versions, three services, preserved PostgreSQL runtime base, preload/worker bounds, absence of auto-install, no secrets and documentation consistency; run architecture checks. The target-server image built and PostgreSQL reached `healthy`; the `pg_available_extensions` query for timescaledb 2.28.3 and vector 0.8.5 remains required and Unverified. Docker execution remains unavailable locally.
- Recovery: before schema activation, rebuild the prior PostgreSQL image while preserving the volume. After either extension is created, downgrade/removal requires a separately approved migration or restore plan; never delete the volume as rollback.

### Approved lightweight middleware capacity adjustment — 2026-07-23

- Outcome: use one smaller, internally consistent capacity profile for architecture deployment testing while retaining the existing three services, versions, secrets and data volumes.
- Acceptance: Compose fallbacks and `.env.example` match; PostgreSQL uses 2 CPU/1 GiB reservation/2 GiB limit with 512 MiB shared buffers, 50 connections, six workers and two TimescaleDB workers; Redis uses 1 CPU/512 MiB reservation/1 GiB limit with 512 MiB `maxmemory`; MinIO uses 1 CPU/512 MiB reservation/1 GiB limit; no reservation exceeds a limit and no internal memory target exceeds its container limit.
- Owner and contracts: platform/operations owns the resource defaults. No service, API, data-owner, dependency, secret, schema, port, volume or disk-plan contract changes.
- Affected files: middleware Compose/environment/runbook, ADR-0009 and active architecture/performance/reliability/governance/intake/task evidence.
- Excluded: product/application code, extension activation, workload claims, production sizing, monitoring implementation, disk mutation and password rotation.
- Verification: statically compare both configuration sources, assert memory/worker relationships and the unchanged three-service/secret/volume contract, run Bash syntax, architecture tests and diff checks; one target-server build/start/health smoke passed, while local Docker execution and representative load measurement remain Unverified.
- Performance and reliability: the profile is for light data and architecture verification only. Concurrent RAG/stock ingestion, indexing, backup and compaction require observation and likely larger values; BuildKit compilation needs separate transient host headroom.
- Recovery: raise values in the untracked server `.env` and recreate affected containers without deleting named volumes; never use `down -v` for capacity rollback.

### Approved MinIO Go Module proxy adjustment — 2026-07-23

- Outcome: make the MinIO builder use the Aliyun Go Module mirror that the user verified from the target server, while keeping the proxy configurable, deterministic and checksum verified without depending on GitHub reachability.
- Acceptance: the inline builder fixes the canonical module version `v0.0.0-20251015172955-9e49d5e7a648`, downloads it with `go mod download`, builds from the returned local directory with explicit release metadata, declares and consumes `GOPROXY`/`GOSUMDB`, and has no VCS/`direct` fallback; Compose arguments and `.env.example` match; `GOSUMDB` is not disabled; MinIO tag, runtime image, secrets and volumes remain unchanged.
- Owner and contracts: platform/operations owns build transport. No runtime service, application dependency, API, data owner or schema changes.
- Affected files: middleware Compose/environment/runbook and active stack/governance/task evidence. ADR and technical debt are N/A because this is a configurable build-network correction within the existing image recipe.
- Verification: assert the exact canonical module and release metadata, escaped inline-Dockerfile variables, module-directory extraction, proxy without `direct`, enabled checksum verification and unchanged service/secret/volume contracts; run Bash syntax, architecture tests and diff checks. The target server first reproduced official-proxy timeout, missing-Git, direct-GitHub and deprecated-version metadata failures, then successfully built the deterministic module-directory recipe and started a healthy MinIO container.
- Recovery: set another trusted module-only `FLOWVERSE_GO_PROXY` in the untracked `.env` or revert the builder recipe and rebuild the image; no runtime data-volume rollback is involved.

### Approved middleware deployment compatibility corrections — 2026-07-23

- Outcome: synchronize the repository with the exact corrections that allowed the approved middleware topology to build and reach three healthy containers on the target server.
- Acceptance: PostgreSQL image verification accepts the official Debian package suffix while still requiring PostgreSQL 18.4; Redis keeps its password file root-only, reads it in a bounded root wrapper, protects the generated configuration and delegates to the official entrypoint so the server process runs as `redis`; MinIO uses the deterministic module-directory build above; no credential value is committed or printed.
- Owner and contracts: platform/operations owns the Compose startup/build boundary. Service count, versions, ports, volumes, capacity, data authority, application dependencies and extension/schema ownership remain unchanged; no ADR is triggered because these are compatibility and least-privilege corrections inside ADR-0007/0008/0009.
- Affected files: `deploy/server/middleware/compose.yml`, `.env.example`, runbook/secret instructions, root README, and active architecture/stack/reliability/performance/governance/task evidence.
- Excluded: `services/**`, local runtime, password values or rotation, extension activation, business schemas/APIs, public exposure, CI/CD, TLS, backup/restore, monitoring, HA and destructive volume operations.
- Reliability/security: root-only secrets remain mode 600; Redis root exists only in the startup wrapper and official entrypoint before process downgrade; health checks remain authenticated and bounded; named volumes remain the recovery boundary and the deployment directory must be retained.
- Verification: statically assert the three compatibility contracts, exact versions, three services/four secrets/three volumes, Bash syntax, architecture checks/self-tests, secret absence and diff hygiene. Target-server image build and three-current-health smoke Passed once; updated one-command rerun, extension SQL query, sustained health, workload capacity and recovery remain Unverified.
- Performance: product interaction and bundle performance are N/A; the source-build path changes first-build behavior, but no controlled before/after build duration or resource measurement exists, so performance remains Unverified.
- Recovery: revert only these source/config/documentation corrections and rebuild/recreate affected containers without `-v`; never delete named volumes or the deployment directory as rollback.

- Confirm exact runtime/framework/version ranges, package manager, bootstrap command, allowed files, and rollback plan.
- Create only approved manifests, lockfiles, configuration, quality/architecture gates, test harnesses, and measurement entry points.
- Import/map UIUX `DesignSpec/tokens.json` into one canonical token mechanism; do not add product behavior.
- Verify install, lint/format, typecheck, unit, integration/contract, E2E, architecture, reliability, build, and performance commands and update their execution state.
- Establish human-confirmed lab environments, measurement noise, baseline-dependent thresholds, and recovery-test entry points; H0 datasets must retain the fixed external-PRD capacity inputs and the 20-outline/3-chapter default above.

## Phase 3: V1.0 Identity, Shell, and Work Home — C01-C04

- Implement default user/admin authentication, first password change, lockout, session expiration, route isolation, and recovery.
- Implement the global shell and P01 regions: shared Bot, continue work, pending summary, and task list with independent loading/failure.
- Implement the Stage 0 `CreationBaseline` and task cockpit with lifecycle/control/visibility/deletion state separation and one server-authoritative next action. Do not require unconfirmed V1.1 operation fields to create or formalize V1.0 novel content.
- Cover ambiguity, action-card revalidation, task switching, Bot failure/policy/queue degradation, and mobile read-only behavior.
- Primary acceptance: AC-01 through AC-05, AC-06A, AC-07, AC-24, AC-26 through AC-30.

## Phase 4: V1.0 References, Creation, Candidates, and Versions — C05-C10

- Implement reference upload/processing, rights/provenance, selected fragments, actual-use trace, Prompt-injection isolation, deletion impact, and allowed formats.
- Implement settings, characters, outline, chapters, candidates, human-edited candidates, Review, disagreements, formal confirmation, work-memory confirmation, complete immutable snapshots, and comparison.
- Implement save/offline/stale/conflict recovery and prevent formal progress after save failure or unresolved blockers.
- Primary acceptance: AC-07, AC-08A, AC-09A, AC-10 through AC-11, AC-24 through AC-31, AC-32A, AC-33A, and applicable AC-34A/AC-35 assertions.

## Phase 5: Cross-Release Lane — Versioned AI Execution and Read-Only Agent Trace — C07-C09

- Implement execution preview, provider/model/policy/version recording, global paid slot, per-task step bound, up-to-three-model fan-out, queue, partial completion, attempts, retry/model switch, timeout, cost, and budget gates.
- Implement read-only Agent execution trace and user checkpoints; do not implement arbitrary wiring, custom DAGs, free Agent creation, or Prompt tuning.
- Verify model/provider data scopes and exclude screenshots from every model request.
- V1.0 enables only governed first-version novel creation/Review workloads and proves AC-19A. V1.1 adds packaging/analysis workloads and proves AC-19B. V1.2 adds formal-decision-driven next-round creation and proves AC-19C. Stage-irrelevant roles must not execute merely to satisfy cumulative counts.
- Primary acceptance: AC-18, AC-19A through AC-19C when first due, AC-20/AC-20A/AC-20B through AC-23, and applicable recovery/performance/reliability rows; every added workload requalifies these assertions.

## Phase 6: V1.1 Packaging, External Release, Feedback, and Single-Cycle Review — C03/C11-C14

- Extend the existing task Stage 0 with a separately user-confirmed `OperationValidationBaseline`; preserve `CreationBaseline`, existing formal snapshots, and audit history. Do not silently backfill platform, metric, observation, validation, or manual-baseline facts.
- Implement AI and human packaging candidates, Review, immutable packaging versions, and release-plan bindings.
- Implement manual external-release facts, evidence, material-difference classification, and atomic actual-release + Cycle creation.
- Implement feedback value union, snapshots/corrections, analysis input lineage, AI analysis candidate, user-confirmed formal analysis, and validity checklist.
- Implement “continue observing” as a standalone observation action that records the next point/reason, creates no formal human-decision record, leaves the Cycle active, and returns to feedback. Implement formal human decision as a separate confirmation path.
- After every ended Cycle, run D12 `cycleTimeReconciliation` and preserve its evidence so whichever Cycle later becomes N in the first adjacent valid pair already has a trustworthy record; this complex action remains unavailable on mobile.
- Drive one rehearsal Cycle with fixtures, then real validation only after external/provider/compliance/recovery gates are confirmed.
- Primary acceptance: AC-06B, AC-08B, AC-09B, AC-12 through AC-15, AC-19B, AC-23, AC-32B through AC-34B, all V1.0 cumulative regression, and every PRD 7.6 validity checklist item for the real Cycle; none of those hard conditions may be waived as N/A. AC-16/AC-17 and two-Cycle mechanism completion remain V1.2 due.

## Phase 7: V1.2 Decision-Driven Creation and Closed-Loop Effect — C06/C11-C14

- Convert only a current user-confirmed formal decision into a bounded next-round plan containing goal, change scope, references, actual Agent/model choices, candidate count, budget, expected change, and next release plan.
- Bind the formal decision and next-round plan into the execution input; AI creates candidates only, and the user separately Reviews and confirms the resulting content snapshot or packaging version.
- Prove that the preceding valid Cycle N decision was implemented as an actual scoped product change included in the adjacent Cycle N+1 external release; preserve the decision → plan → execution → candidate → formal version → release lineage without claiming that the change caused an external metric outcome.
- Complete the latter Cycle N+1 in the first adjacent valid pair, adjacent-Cycle comparability classification, non-causal outcome labels, individual-value calculation, and the following-Cycle entry. Normal success may be 1→2→3, but invalid Cycle numbers are never renumbered.
- Repeat D12 `cycleTimeReconciliation` for Cycle N+1 and add the V1.2 `twoCycleSurvey`; only the simple survey is available as the package-defined mobile write exception.
- Primary acceptance: AC-16, AC-17, AC-19C, AC-32C through AC-34C, full AC-01 through AC-35 cumulative regression, all PRD 7.5/7.6 rows, and applicable UIUX scenarios.

## Phase 8: Cross-Release Lane — Governance Surfaces, Export, Deletion, and Operations — C15-C18

- Complete the four mutually exclusive drawers, activity popover, configuration versions, model/cost policy, compliance/platform rules, monitoring, audit, and bounded debug access.
- Implement three approved export packages, task controls, deletion/retention, backup/restore, and audit cleanup.
- Verify administrators cannot bypass compliance or perform user formal actions.
- Qualify each governance/export/recovery capability at the release that first consumes it: AC-32A/33A/34A in V1.0, AC-32B/33B/34B in V1.1, and AC-32C/33C/34C in V1.2. Later release evidence must include earlier-history preservation.
- Primary acceptance: AC-31 through AC-35 and their versioned children.

## Phase 9: Per-Release H0/H1/H2 Gates and Real-World Validation

- At every release, complete the version-level traceability gate above and map every due AC/child assertion and approved UIUX scenario to exact evidence. At V1.2, close every PRD 7.5 row, PRD 7.6 Cycle check, AC-01 through AC-35, and UIUX scenario 1-130.
- Run Phase 9 once for H0 before V1.0 release, again for H1 before V1.1 release, and again for H2 before V1.2 release; a later run cannot retrospectively qualify an earlier release.
- H0 evidence includes its separate business and operational physical allow/deny manifests; negative router/build/dependency evidence that the Check/public-chain/internal-status diagnostic trio is absent while exact `OPS-API-001..003/OPS-WORKER-001..002` remain operational-only; every V1.0 child/scenario ref; first formal snapshot rebuild/compare/export; backup/restore/delete-non-resurrection exercise; mandatory `DataSafetyGate`; and the fixed-input benchmark report with every still-pending profile field visible. `AvailabilityGate` evidence is included only when `UD-AVL-01` makes it applicable.
- H1 evidence includes the complete H0 regression, updated allow/deny manifest, preserved H0 history, one real valid Cycle, and negative evidence that continued observation or an invalid Cycle does not satisfy completion; every newly affected provider, Prompt, object, degradation, performance and recovery row is requalified.
- H2 evidence includes complete H0/H1 regression, updated allow/deny manifest, the first adjacent valid Cycle N/N+1 lineage, comparison classification, individual-value result, following Cycle N+2 path, and row-level PRD 7.5/7.6, AC-01-35 and UIUX 1-130 closure.
- Run all Confirmed repository checks and due reliability/performance/security/accessibility/recovery gates without using an unapproved 99.9% topology to fail H0 or using `DataSafetyGate` evidence to claim HA.
- Capture required visual evidence at 1440 × 900, 1280 × 720, and 390 × 844.
- Rehearse failure, timeout, duplicate, partial success, restart, restore, stale input, saturation, provider-policy change, and deletion paths.
- V1.0 completes the first formal novel snapshot without claiming release/Cycle completion. V1.1 completes one real valid Cycle and may not count “continue observing” as a decision or completed review outcome.
- V1.2 completes two consecutive valid real Cycles and records serious trust incidents separately from functional completion.
- Report mechanism result and individual-value result without claiming causality or market validation; V1.0/V1.1 must not publish those final V1.2 claims early.

### Approved local middleware authentication diagnostic — 2026-07-29

- Outcome: configure the ignored local environment without echoing secrets and prove authenticated access to the server PostgreSQL, Redis and MinIO through the existing loopback SSH forwards.
- Acceptance: PostgreSQL executes `SELECT 1`; Redis accepts `AUTH` and returns `PONG`; MinIO accepts a signed read-only `ListBuckets`; every check is bounded, has no retry, prints no secret or response body, and the command exits non-zero unless all three are ready.
- Owner/contracts: the API health package owns the diagnostic; the platform wrapper only delegates. No business schema, Redis key/queue, MinIO bucket/object, application root account or public HTTP contract is added.
- Affected files: API diagnostic settings/source/tests, local PowerShell configuration/launcher files, `.env.example`, runbooks and active architecture/stack/reliability/intake/decision evidence.
- Excluded: server Compose, public ports, firewall/security groups, business code, Web UI, Worker behavior, migrations/extensions, TLS, production access and new dependencies.
- Performance/reliability/security: three checks run concurrently with a three-second default and ten-second maximum, zero retry and truthful classified failure; local plaintext credentials remain in ignored `.env` and are never logged. Product interaction and bundle performance are N/A.
- Verification: API Ruff/Pyright/pytest, PowerShell parsing, architecture checks/self-tests, configuration-failure execution, live credentialed execution, local service-chain smoke and diff/secret review.
- Recovery: delete the ignored root `.env` and revert the diagnostic/settings/launcher changes; server containers, volumes and data remain untouched.

## File-Level Planning Rule

Before each approved implementation slice, replace its phase bullets with or append a scoped plan that names:

- exact parent/child acceptance and evidence IDs, first-due release, cumulative regression scope, and user-visible result;
- files changed and explicitly excluded;
- module/data owner, public contracts, dependency edges, and compatibility class;
- security, privacy, accessibility, reliability, performance, release-order, and recovery impact;
- ADR/debt changes and exact focused/full verification commands.

Do not invent source paths before the bootstrap establishes them.

## Stop Conditions

- The active approval scope is not APPROVED, or a required target/runtime/version/command/contract remains Unknown.
- A product/UIUX requirement conflicts with the approved package or needs new human judgment.
- The due release lacks the version-level traceability artifact, a parent AC is treated as Passed from an incomplete child set, or a deferred requirement is silently marked Passed/N/A.
- The release manifest omits its physical allow/deny list, an out-of-version route/action can create state, `DataSafetyGate` is conflated with `AvailabilityGate`, or a 99.9%/HA claim lacks `UD-AVL-01` and its evidence.
- Any applicable `UD-PG-01` through `UD-PERF-01` decision remains unrecorded, or H0 performance evidence omits one of the fixed PRD capacity inputs while its environment/concurrency/sample/threshold profile remains implicit.
- A V1.0 task would require V1.1 operation facts to formalize initial novel content, a V1.1 upgrade would rewrite prior formal history, or “continue observing” would create a formal decision/close a Cycle.
- Work requires an unapproved dependency, API, schema, auth, provider, architecture, deployment, security, sensitive-data, destructive, or budget decision.
- A production dependency cycle, private cross-owner access, second source of truth, mutable formal-history overwrite, or release/Cycle inconsistency would be introduced.
- A due reliability/performance/security/recovery gate is missing, Unverified, Failed, or exceeds its Confirmed target.
