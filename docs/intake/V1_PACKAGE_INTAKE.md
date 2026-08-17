# FlowVerse V1 Package Intake

## Package Review State

**IN_REVIEW**

This global state describes receipt/review of the latest package revision. Code gates read the matching row in Approval Scopes, not this global state.

Allowed transitions:

- AWAITING_PACKAGE → IN_REVIEW
- IN_REVIEW → BLOCKED or APPROVED
- BLOCKED → IN_REVIEW after new evidence or a user decision
- APPROVED → IN_REVIEW when a revised package changes approved facts
- Any replaced package revision → SUPERSEDED

- Only the user may approve an intake scope or resolve product and architecture conflicts.
- Do not write business code before the state is APPROVED for that implementation slice.
- A non-business engineering bootstrap may begin after the bootstrap scope, target stack, and exact bootstrap plan are approved.
- If the package contains source, determine whether it is the implementation baseline or reference material before editing it.
- The 2026-08-12 roadmap direction and 2026-08-13 documentation-sync authorization do not replace this implementation gate: proposed repository amendments, UIUX deltas, Prompts, technical decisions, APIs, Schemas, dependencies, ADRs, and acceptance claims remain blocked until their exact scopes receive final human approval.

## Approval Scopes

| Scope ID | Package revision | Scope type and description | State | Exact evidence / decision | Approved by and date | Deferred unrelated Unknowns |
|---|---|---|---|---|---|---|
| FV1-PRODUCT-DESIGN | PRD v1.1 / UIUX Phase 1 | Product scope, user journeys, UIUX contracts, design tokens, product acceptance, and product non-functional requirements | APPROVED | User selected the external PRD/UIUX package as the new authority, 2026-07-13; package hashes below | User, 2026-07-13 | Runtime, architecture, API, schema, provider contracts, deployment, executable commands |
| FV1-ROADMAP-DIRECTION | User roadmap decision 2026-08-12 | Named delivery direction only: V1.0 novel scenario; V1.1 AI content analysis/operations review; V1.2 AI content creation/operations closed-loop effect; V2.0 stock/fund/futures research analysis/review | APPROVED | Explicit user messages in the current FlowVerse technical-solution conversation, 2026-08-12 | User, 2026-08-12 | Exact release scope and completion gates, UIUX scenario split, Prompt contracts, V2 domain/compliance/data scope, architecture, API, Schema, dependencies, deployment, SLOs, implementation and acceptance results |
| FV1-ROADMAP-REVIEW | Repository roadmap change set 2026-08-13 | Authorize drafting and synchronizing a repository PRD amendment, product/acceptance/implementation-plan summaries, versioned UIUX guidance, technical proposal, and system-decision Prompt proposal, then perform an overall review | IN_REVIEW | User requested the synchronized document revision and final overall review in the current conversation, 2026-08-13; artifact inventory below | User authorized editing/review, not final content approval, 2026-08-13 | External PRD/ZIP mutation, implementation release, AC/UIUX pass, accepted ADR, business API/Schema, dependency/runtime selection, production topology, HA/performance result, and financial-domain implementation |
| FV1-DOCUMENT-COMPLETION | Repository completion pass 2026-08-15/16 | Authorize filling the in-repository PRD amendment, UIUX/acceptance overlays, detailed technical design, decision records and delivery gates from the adversarial review, followed by another cross-document review | IN_REVIEW | User explicitly requested repository PRD, UIUX and detailed technical-solution completion and then asked to continue unfinished work, 2026-08-15/16; exact artifacts below | User authorized document edits/review, not final content approval, 2026-08-15/16 | External PRD/ZIP mutation, Accepted ADR, dependency/API/Schema/auth/runtime approval, business implementation, production deployment, HA/performance/recovery result, Prompt activation and financial implementation |
| FV1-ARCH-BASELINE | Service-directory decision 2026-07-15 | Separate Web, API and Worker code services; singular module ownership; PostgreSQL operational dependency; no direct cross-service source imports | APPROVED | User explicitly required service-based directories and code in separate modules on 2026-07-15; ADR-0002 supersedes ADR-0001 | User, 2026-07-15 | Business schemas and APIs, authentication, asynchronous API/Worker contract, AI/provider contracts, object-storage provider, executable production CD and unmeasured scale |
| FV1-BOOTSTRAP | Service bootstrap decision 2026-07-15 | Non-business Web/API/Worker service skeleton under `services/`; API native runtime and Worker check; separate manifests/locks/images, health/logging/migration entry points, architecture checks and tests | APPROVED | User instruction on 2026-07-15 approves the service-directory boundary; implementation evidence is recorded in the engineering registries | User, 2026-07-15 | Every product behavior and product acceptance slice; Web source/lock/runtime; long-running Worker; object-storage runtime; Redis/message broker; bound cloud execution/CD; production SLO verification |
| FV1-DELIVERY-BOOTSTRAP | Yunxiao delivery decisions 2026-07-15/16 | Historical Yunxiao Flow, ACR and host Docker delivery scope | SUPERSEDED | Replaced by the user's local-test-only deployment decision on 2026-07-21; ADR-0006 supersedes ADR-0003 and the delivery portions of ADR-0004/0005 | User, superseded 2026-07-21 | Any future CI/CD or production target requires a new decision |
| FV1-LOCAL-RUNTIME | Native local-start decision 2026-07-16 | Local development runs native Python/Node processes; root Compose is removed; PostgreSQL is independently supplied through configuration | APPROVED | User explicitly required direct local startup without Docker on 2026-07-16; ADR-0004; completed by ADR-0005/0006 | User, 2026-07-16/21 | PostgreSQL installation/provisioning and any future production topology |
| FV1-DIAGNOSTIC-BOOTSTRAP | Deployment-verification decision 2026-07-20 | Non-business Web Check page, synchronous API-to-Worker readiness diagnostic and native three-service startup | APPROVED | User instructed Codex to fix all reviewed issues so the architecture can be locally deployment-verified; ADR-0005 with production-delivery portion superseded by ADR-0006 | User, 2026-07-20/21 | Business execution, authentication, PostgreSQL provisioning and production delivery |
| FV1-LOCAL-TEST-DEPLOY | Local deployment replacement 2026-07-21 | Remove the Yunxiao repository deployment directory and provide one native local test deployment command | APPROVED | User explicitly requested local startup/deployment for testing instead of Yunxiao; ADR-0006 | User, 2026-07-21 | CI/CD, staging/production environment and remote rollout/rollback |
| FV1-REMOTE-MIDDLEWARE-DEV | Local-to-server development access decision 2026-07-24 | Add an optional Windows OpenSSH local-port-forward helper so native local development can reach the private server PostgreSQL, Redis and MinIO ports without changing their loopback-only Compose bindings | APPROVED | User explicitly required the deployed middleware to support native local development; the implementation preserves the already approved private-port security boundary | User, 2026-07-24 | Public middleware exposure, SSH account/key provisioning, firewall/security-group mutation, application Redis/MinIO consumers, TLS, production remote-access policy |
| FV1-LOCAL-MIDDLEWARE-DIAGNOSTIC | Local middleware authentication decision 2026-07-29 | Securely configure the ignored local environment and authenticate PostgreSQL, Redis and MinIO through the approved SSH forwards using read-only/non-mutating probes | APPROVED | User explicitly requested local configuration and an end-to-end access run for all three middleware services; ADR-0010 | User, 2026-07-29 | Business schemas, Redis cache/queue keys, MinIO buckets/object operations, application root credentials, public exposure, TLS and production remote-access policy |
| FV1-SERVER-MIDDLEWARE-DEPLOY | Server middleware/capacity decisions 2026-07-22/23 | One server-only Docker Compose project for PostgreSQL, Redis and MinIO with untracked file secrets, persistent volumes, health checks and lightweight test resource limits; native local application startup remains unchanged | APPROVED | User explicitly requested these three services with memory/disk planning and no committed passwords, then approved the smaller internally consistent test profile; ADR-0007/0009 | User, 2026-07-22/23 | Application consumers and connection values, business schemas, buckets/users, cache contracts, measured workload capacity, CI/CD, application production deployment, TLS, backups/restore, monitoring and high availability |
| FV1-SERVER-DATA-EXTENSIONS | PostgreSQL extension/capacity decisions 2026-07-22/23 | Package pgvector and TimescaleDB OSS together in the existing PostgreSQL 18.4 image for future simple RAG and stock time-series use; preload with lightweight bounded workers; do not automatically create extensions or business schemas | APPROVED | User explicitly requested pgvector and TimescaleDB together, then approved the smaller worker profile; ADR-0008/0009 | User, 2026-07-22/23 | `CREATE EXTENSION` migrations, embedding model/dimension/index, RAG ingestion, market schemas/hypertables, retention/compression policies, application consumers, backup/restore and measured performance |

Each scope row follows the same review transitions independently. A revised package moves only affected rows back to IN_REVIEW; unaffected APPROVED rows remain valid unless the user supersedes them.

APPROVED accepts the package revision and named scope; it does not claim every future subsystem is fully specified. Unknown facts outside the active scope remain deferred and do not block unrelated work.

`FV1-ROADMAP-DIRECTION` confirms only the named roadmap order and themes. `FV1-ROADMAP-REVIEW` and `FV1-DOCUMENT-COMPLETION` control the synchronized change set and remain `IN_REVIEW`; therefore neither can release business implementation, mark a product/UIUX acceptance row Passed/N/A, activate a Prompt, or accept an architecture decision. The existing `FV1-PRODUCT-DESIGN` baseline stays approved and unchanged while this overlay is reviewed.

## Receipt Record

| Field | Value |
|---|---|
| Package name | FlowVerse PRD v1.1 + FlowVerse Phase 1 AI 长篇小说创作工作台 UIUX MVP |
| Original location | `D:\流域\FlowVerse_V1_需求分析与产品方案_PRD.md`; `D:\流域\FlowVerse_UIUX_MVP.zip` |
| Received date and timezone | Reviewed 2026-07-13, Asia/Shanghai (UTC+08:00) |
| Size and file count | PRD: 214,399 bytes, 1 file; UIUX ZIP: 10,569,381 bytes, 98 entries |
| Integrity hash | PRD SHA-256 `760BA720382C2AF8648E0378C74623AF33D85E09407ED965C81A0F0F1467F049`; ZIP SHA-256 `470AF5B00E52BCA3B883AF67D801A3FE4A21595DC09DCB9637937B63DB2B17DD` |
| Declared V1 revision | PRD v1.1, finalized 2026-07-12; UIUX package generated 2026-07-12 |
| User-designated authority | Product and UIUX authority, explicit user decision 2026-07-13 |

Preserve the original package unchanged. Extract or convert only into a separate working location.

The 2026-08-13 roadmap review is an in-repository overlay and does not create a new external package receipt or hash. The PRD/ZIP names, sizes, file counts, dates, integrity hashes, and 2026-07-13 approval above remain exactly the receipt for the authoritative originals.

References in PRD v1.1 to a v0.8 direction brainstorm describe document provenance only. No v0.x application, implementation baseline, migration source, upgrade path, or compatibility requirement is approved.

## Artifact Inventory and Classification

| Artifact | Classification | Approved scope | Evidence / notes |
|---|---|---|---|
| `FlowVerse_V1_需求分析与产品方案_PRD.md` | Authoritative specification | Product scope, flows, states, acceptance, product NFRs, and product constraints on later architecture | Header: PRD v1.1; sections 3, 4, 5, 6, 7, and 8 |
| UIUX `README.md` | Authoritative design overview | Phase 1 information architecture, design principles, responsive policy, and workflow-visualization boundary | ZIP root README |
| `DesignSpec/pages.json` | Authoritative design contract | Page/surface contracts, states, route intent, component composition, and responsive behavior | Contract examples do not approve backend APIs or routes as implementation contracts |
| `DesignSpec/components.json` | Authoritative design contract | Component/state requirements | Component names are design identifiers, not evidence of source modules |
| `DesignSpec/tokens.json` | Authoritative design contract | Semantic visual tokens, breakpoints, typography, motion, and accessibility | Canonical design input for later approved frontend bootstrap |
| `DesignSpec/state_matrix.json` | Authoritative acceptance inventory | 130 UIUX scenarios and screenshot coverage mapping | Test implementation remains NotYetImplemented |
| `DesignSpec/interaction.md`, `workflow.md`, `frontend-handoff.md`, `frontend-types.ts` | Reference with normative product constraints | Interaction semantics, formal-action safety, read-only Agent trace, and candidate/formal boundaries | Suggested routes, TypeScript shapes, request names, and libraries require engineering approval |
| `UI设计稿/` and `Prototype/` | Authoritative visual reference | 63 screenshots, responsive examples, and clickable interaction reference | Reference material, not runnable product source or implementation baseline |
| `Source/` | Package validation tooling reference | Package-only rendering and validation | Not repository tooling; commands are not approved project commands |
| `DesignSpec/validation-report.json` | Generated output | Package self-check only | Reports passed, but multiple passing checks contain missing/not-found detail; cannot prove package completeness or repository acceptance alone |

### Repository Roadmap Change Set — 2026-08-13

These artifacts are outside the immutable external-package receipt. They are classified together because product, UIUX, Prompt and architecture boundaries must be reviewed as one change set:

| Artifact | Classification / state | Review scope | Gate / non-claim |
|---|---|---|---|
| `../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md` | Draft amendment — `IN_REVIEW` | Proposed V1.0/V1.1/V1.2 partition, baseline split, D/S/H authority and roadmap decisions | Does not amend the approved PRD until final overall human approval |
| `../product/PRODUCT_POSITIONING.md`, `../product/V1_PRODUCT_BRIEF.md`, `../uiux/ACCEPTANCE_CRITERIA.md`, `../tasks/V1_IMPLEMENTATION_PLAN.md` | Synchronized repository summaries — `IN_REVIEW` for the roadmap delta | Proposed release outcomes, cumulative AC children, traceability gate and staged plan | Existing approved package behavior remains the fallback; no business slice is released by these edits |
| `../uiux/UIUX_PRINCIPLES.md`, `../uiux/INTERACTION_RULES.md`, `../uiux/COPY_RULES.md`, `../uiux/DESIGN_TOKENS.md`, `../uiux/RELEASE_CAPABILITY_MATRIX.md`, `../uiux/SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md` | Versioned UIUX guidance and first-due registry — `IN_REVIEW` | Proposed capability/route, decision-candidate, Prompt-governance, responsive/copy/token deltas, explicit system degradation/freshness/retry/recovery contract, and scenario 1-130 first-due/cumulative map | Mapping and contracts are review evidence only; implementation must supply exact visual/behavior/a11y evidence. No visual or behavioral pass is claimed |
| `../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md`, `../engineering/ARCHITECTURE_BASELINE.md`, `../engineering/RELIABILITY_BUDGET.md`, `../engineering/PERFORMANCE_BUDGET.md` | Engineering proposal and synchronized target registries — `Proposed / IN_REVIEW` | Proposed V1.0-V2.0 architecture, HA/performance/recovery direction, contracts, target rows and decision backlog | Requires applicable Accepted ADRs, frozen targets and human approval; proves no API, Schema, dependency, deployment, SLO, performance, HA or recovery result |
| `../engineering/V1_DETAILED_TECHNICAL_DESIGN.md`, `../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`, `../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`, `../engineering/V1_FRONTEND_TECHNICAL_DESIGN.md` | Detailed engineering design package — `Proposed / IN_REVIEW` | Three-service stack and boundaries, middleware/operations, logical tables and constraints, REST/SSE/internal/object contracts, frontend routes/state/protocols, Prompt binding integration and release slices | Detailed enough to review and later derive DDL/OpenAPI/tasks, but does not approve or implement dependencies, API, Schema, auth, topology, budgets, Prompt activation or product behavior |
| `../engineering/V1_TECHNICAL_SOLUTION_EVALUATION.md`, `../engineering/V1_TECHNICAL_SOLUTION_ADVERSARIAL_REVIEW.md` | Cross-document and adversarial review results — `Conditional / Advisory` | Record consistency findings, current-vs-target facts, quality-attribute assessment, implementation blockers and proposed closure plan | Do not change either review scope from `IN_REVIEW`, accept an ADR, release implementation, or prove Prompt/UIUX/HA/performance/recovery results |
| `../ai/SYSTEM_DECISION_PROMPTS.md` | Prompt specification — `IN_REVIEW / Proposed` | Proposed deterministic/semantic/human authority, Prompt families, schemas, evaluation and activation gates | No family, taxonomy, Schema or Prompt version is implemented, HumanApproved, Active, or production-authorized |
| `../decisions/ADR-0011-*.md` through `ADR-0024-*.md` where files exist, `ADR-0029-*.md`, `ADR-0030-*.md`, and `DECISION_LOG.md` | Architecture decision candidates — `Proposed` | Module ownership/slices, API/degradation, async/Worker, auth, ObjectStore, Agent/provider, immutable versions, recovery/deletion, frontend, production delivery, Schema evolution, HA, performance, release activation and Prompt/D-S-H governance | User/TBD remains decision owner; glob-like inventory notation does not create missing ADR-0025～0028, and a Proposed ADR is not architecture approval or implementation evidence |

Final acceptance of these review scopes requires a cross-document conflict review, exact mapping of every affected original PRD/UIUX/AC requirement, applicable Accepted ADRs, and explicit human approval. Until then, implementation gates must not treat any row in this subsection as `APPROVED` evidence.

## Intake Conclusions

- Product/design scope is approved and supersedes the previous repository product/UIUX interpretation.
- The package contains no approved application source, manifest, lockfile, runtime, backend implementation, database, deployment configuration, or repository command.
- The external PRD/UIUX package itself authorizes no React/TypeScript/Python version, dependency, or command. Later approved diagnostic-bootstrap decisions separately Confirm the exact existing runtime/version/command rows in `../engineering/TECH_STACK.md`; those rows apply only to their recorded bootstrap scope. Product router/editor/UI dependencies and every new business dependency remain Proposed or Unknown until separately approved.
- Architecture must preserve the PRD 7.11 invariants, but module boundaries, APIs, schemas, queues, caches, storage, providers, and deployment topology require Proposed ADRs and user acceptance.
- UIUX self-validation anomalies are recorded as a package-quality risk; exact asset and scenario verification remains required before implementation acceptance.
- Independent intake verification on 2026-07-13 confirmed 98 ZIP entries, 6 JSON files, 63 PNG files, all named core artifacts above, and 130 continuously numbered state scenarios from 1 through 130. This verifies inventory only, not product implementation or visual correctness.

## Artifact Classification

Classify every artifact as one of:

- Authoritative specification
- Implementation baseline
- Reference
- Draft
- Example
- Generated output
- Historical material, only when the user explicitly identifies it as historical

Record exact path, type, status, scope, dependencies, and conflicts. Do not treat visual similarity or filename wording as authority.

## Required Inventory

### Product and Design

- Product scope, user journeys, pages, navigation, states, copy, and acceptance
- Design files, frames, components, tokens, breakpoints, motion, accessibility, and responsive behavior
- Fonts, icons, images, illustrations, licenses, export rules, and source-of-truth ownership
- Empty, loading, error, offline, recovery, permission, destructive, and unsaved states

### Engineering

- Source roots, manifests, lockfiles, runtime, language, frameworks, build tools, and package manager
- Users/load/data scale, team expertise, phase roadmap, domain complexity, real-time, compliance, budget, and deployment constraints needed for architecture decisions
- Module boundaries, owners, dependency direction, public contracts, data/invariant ownership, process/deployment boundaries, and external adapters
- Routing, state, data access, editor, API/schema, backend, database, auth, AI provider/SDK, and storage
- Lint, format, typecheck, unit, integration, E2E, build, performance, CI/CD, deployment, and observability
- Existing architecture decisions, compatibility promises, temporary paths, TODO/FIXME/HACK, and baseline technical debt
- Environment variable names and configuration contracts without recording secret values

### Performance and Operations

- Target browsers, devices, CPU, network, cache state, data scale, document size, concurrency, and session duration
- Bundle/asset budgets, route readiness, input/background persistence when specified, API, AI latency/cost, memory, and regression thresholds
- Critical flows, availability SLI/SLO, error budget, RTO/RPO, capacity, timeout/retry/idempotency, degradation, isolation, health, and failure-test requirements
- Privacy, security, retention, backup/restore evidence, recovery, rate-limit, cancellation, rollout, rollback/forward recovery, and operational ownership

## Required Outputs

- Update ../governance/EVIDENCE_POLICY.md evidence records for material decisions.
- Populate ../engineering/TECH_STACK.md with Confirmed, Conflict, Unknown, or N/A entries.
- Populate ../engineering/ARCHITECTURE_BASELINE.md without inventing modules or dependencies.
- Classify applicable targets and controls in ../engineering/RELIABILITY_BUDGET.md.
- Initialize baseline entries in ../engineering/TECH_DEBT_REGISTER.md and register any Proposed ADR in ../decisions/DECISION_LOG.md.
- Reconcile ../product/V1_PRODUCT_BRIEF.md and ../uiux/ without silently overriding current user instructions.
- Confirm project-specific entries in ../engineering/PERFORMANCE_BUDGET.md.
- Convert ../tasks/V1_IMPLEMENTATION_PLAN.md into a file-level plan.
- List missing evidence, conflicts, assumptions, exclusions, and user decisions.

## Approval Gate

Intake can become APPROVED only when:

- Inventory and artifact classification are complete for the approved scope.
- Product, design, implementation-baseline, and source-of-truth ownership are explicit for that scope.
- Architecture context needed by the selected patterns is Confirmed or the pattern is deferred.
- Task-relevant architecture target rows are Confirmed or N/A; implementation conformance may remain NotYetImplemented until the approved slice is built.
- Reliability Applicability is classified as Required, Optional, or N/A for the due scope; required target/verification states follow their Gate stage.
- Target technology, target version/range, bootstrap command, API, asset, and environment decisions required by the first approved slice are Confirmed or N/A.
- Resolved installed versions and generated project commands may remain NotYetInstalled / NotYetAvailable until the approved engineering bootstrap.
- The measurement plan and environment needed to establish initial lab budgets are approved; baseline-dependent thresholds have an explicit post-bootstrap confirmation gate.
- Required reliability target, recovery, capacity, observability, and failure-test plans have an explicit confirmation gate.
- Conflicts and missing decisions that affect the approved scope are resolved by the user.
- Acceptance criteria map to package evidence and a bootstrap or file-level implementation plan.
