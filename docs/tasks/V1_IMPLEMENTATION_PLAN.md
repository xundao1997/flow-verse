# FlowVerse V1 Implementation Plan

## Status

- Product/design scope `FV1-PRODUCT-DESIGN` is approved from PRD v1.1 and the FlowVerse Phase 1 UIUX MVP package.
- Architecture and non-business bootstrap scopes are approved through `FV1-LOCAL-TEST-DEPLOY`. Web/API/Worker source, locks, diagnostic contracts, quality gate and native local-test deployment wrapper are implemented; real PostgreSQL remains an external verification gate, while CI/CD, test-server and production deployment targets are Unknown.
- No business implementation may begin until the relevant architecture targets, technology versions, commands, file scope, acceptance mapping, and due reliability/performance gates satisfy `../engineering/AI_CODING_WORKFLOW.md`.
- V1 is the first implemented release. Direction-document provenance creates no migration or legacy compatibility work.

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

- Confirm exact runtime/framework/version ranges, package manager, bootstrap command, allowed files, and rollback plan.
- Create only approved manifests, lockfiles, configuration, quality/architecture gates, test harnesses, and measurement entry points.
- Import/map UIUX `DesignSpec/tokens.json` into one canonical token mechanism; do not add product behavior.
- Verify install, lint/format, typecheck, unit, integration/contract, E2E, architecture, reliability, build, and performance commands and update their execution state.
- Establish approved lab environments, datasets, measurement noise, baseline-dependent thresholds, and recovery-test entry points.

## Phase 3: Identity, Shell, and Work Home — C01-C04

- Implement default user/admin authentication, first password change, lockout, session expiration, route isolation, and recovery.
- Implement the global shell and P01 regions: shared Bot, continue work, pending summary, and task list with independent loading/failure.
- Implement Stage 0 and task cockpit with lifecycle/control/visibility/deletion state separation and one server-authoritative next action.
- Cover ambiguity, action-card revalidation, task switching, Bot failure/policy/queue degradation, and mobile read-only behavior.
- Primary acceptance: AC-01 through AC-07, AC-24, AC-26 through AC-30.

## Phase 4: References, Creation, Candidates, and Versions — C05-C10

- Implement reference upload/processing, rights/provenance, selected fragments, actual-use trace, Prompt-injection isolation, deletion impact, and allowed formats.
- Implement settings, characters, outline, chapters, candidates, human-edited candidates, Review, disagreements, formal confirmation, work-memory confirmation, complete immutable snapshots, and comparison.
- Implement save/offline/stale/conflict recovery and prevent formal progress after save failure or unresolved blockers.
- Primary acceptance: AC-07 through AC-11, AC-24 through AC-32.

## Phase 5: AI Execution and Read-Only Agent Trace — C07-C09

- Implement execution preview, provider/model/policy/version recording, global paid slot, per-task step bound, up-to-three-model fan-out, queue, partial completion, attempts, retry/model switch, timeout, cost, and budget gates.
- Implement read-only Agent execution trace and user checkpoints; do not implement arbitrary wiring, custom DAGs, free Agent creation, or Prompt tuning.
- Verify model/provider data scopes and exclude screenshots from every model request.
- Primary acceptance: AC-18 through AC-23 and applicable recovery/performance/reliability rows.

## Phase 6: Packaging, External Release, Feedback, and Cycle — C11-C14

- Implement immutable packaging versions and release-plan bindings.
- Implement manual external-release facts, evidence, material-difference classification, and atomic actual-release + Cycle creation.
- Implement feedback value union, snapshots/corrections, formal analysis, continue observing, validity checklist, human decision, next-round plan, and Cycle comparison.
- Drive one rehearsal Cycle with fixtures, then real validation only after external/provider/compliance/recovery gates are confirmed.
- Primary acceptance: AC-12 through AC-17, AC-23, AC-33, and PRD 7.6.

## Phase 7: Governance Surfaces, Export, Deletion, and Operations — C15-C18

- Complete the four mutually exclusive drawers, activity popover, configuration versions, model/cost policy, compliance/platform rules, monitoring, audit, and bounded debug access.
- Implement three approved export packages, task controls, deletion/retention, backup/restore, and audit cleanup.
- Verify administrators cannot bypass compliance or perform user formal actions.
- Primary acceptance: AC-31 through AC-35.

## Phase 8: Release and Real-World Validation

- Map all PRD 7.5 rows, PRD 7.6 Cycle checks, AC-01 through AC-35, and UIUX scenarios 1-130 to exact evidence.
- Run all Confirmed repository checks and due reliability/performance/security/accessibility/recovery gates.
- Capture required visual evidence at 1440 × 900, 1280 × 720, and 390 × 844.
- Rehearse failure, timeout, duplicate, partial success, restart, restore, stale input, saturation, provider-policy change, and deletion paths.
- Complete two consecutive valid real Cycles and record serious trust incidents separately from functional completion.
- Report mechanism result and individual-value result without claiming causality or market validation.

## File-Level Planning Rule

Before each approved implementation slice, replace its phase bullets with or append a scoped plan that names:

- exact acceptance/evidence IDs and user-visible result;
- files changed and explicitly excluded;
- module/data owner, public contracts, dependency edges, and compatibility class;
- security, privacy, accessibility, reliability, performance, release-order, and recovery impact;
- ADR/debt changes and exact focused/full verification commands.

Do not invent source paths before the bootstrap establishes them.

## Stop Conditions

- The active approval scope is not APPROVED, or a required target/runtime/version/command/contract remains Unknown.
- A product/UIUX requirement conflicts with the approved package or needs new human judgment.
- Work requires an unapproved dependency, API, schema, auth, provider, architecture, deployment, security, sensitive-data, destructive, or budget decision.
- A production dependency cycle, private cross-owner access, second source of truth, mutable formal-history overwrite, or release/Cycle inconsistency would be introduced.
- A due reliability/performance/security/recovery gate is missing, Unverified, Failed, or exceeds its Confirmed target.
