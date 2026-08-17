# FlowVerse Evidence Policy

## Purpose

- Every implementation claim must trace to concrete evidence.
- Unknown facts remain Unknown; inference never becomes project fact through repetition.
- Evidence authorizes conclusions only within its stated scope.

## Authority by Fact Type

| Fact type | Authority order |
|---|---|
| Product intent and authorization | Current explicit user decision about that fact → user-approved V1 package or decision record → repository product specification |
| Expected behavior | Approved product brief and acceptance criteria → approved interaction/design rules → current tests and code as evidence of current behavior only |
| Approved target stack, version, or command | Current explicit user decision → approved V1 package → approved architecture/engineering decision |
| Approved architecture decision | Current explicit user decision → Accepted ADR → approved V1 package evidence |
| Current implementation fact | Source, tests, config, CI, manifest, lockfile → engineering documentation → nearby established code pattern |
| Current module, dependency, contract, and data ownership | Source/config/deployment evidence plus Confirmed ../engineering/ARCHITECTURE_BASELINE.md; a target ADR alone does not prove runtime state |
| Resolved installed version | Lockfile → installed metadata → manifest range; never memory or “latest” |
| Currently executable command and directory | Bootstrap: approved exact target command plus tool/environment verification; after bootstrap: checked-in script/config/CI plus environment verification |
| Design asset and copy | Current explicit user decision → approved V1 package artifact → approved repository design/copy specification |
| Performance target | Current explicit user decision → approved package budget → approved project performance registry |
| Performance result | Raw same-environment measurement tied to build, scenario, command, and output; a target or budget never proves a result |
| Reliability target | Current explicit user decision → approved package requirement → Confirmed ../engineering/RELIABILITY_BUDGET.md entry |
| Reliability, recovery, or failure-test result | Raw monitoring/test/restore evidence tied to build, environment, scenario, command, and output |
| Technical-debt acceptance or extension | Current explicit user decision recorded in ../engineering/TECH_DEBT_REGISTER.md; AI may only propose |

## Evidence Status

- Confirmed: directly supported by a precise source.
- Conflict: authoritative sources disagree.
- Unknown: required evidence is absent.
- N/A: proven outside the current scope.
- Assumption: explicitly labeled hypothesis used only for discussion, never implementation authorization.
- Proposed / IN_REVIEW: a reviewable repository change or decision candidate that has not received final human approval; it cannot authorize implementation, acceptance, deployment, or performance/reliability claims.

`Confirmed` applies only to the exact fact stated. In particular, a confirmed roadmap direction or document-editing authorization does not make the resulting product, UIUX, Prompt, architecture, API, Schema, dependency, release gate, or implementation detail approved.

## Evidence Record

Record material conclusions during V1 package intake and task planning:

| Claim | Fact type | Status | Exact evidence path and field | Conflict or gap | Decision owner |
|---|---|---|---|---|---|
| PRD v1.1 and the FlowVerse Phase 1 UIUX MVP package are the V1 product/design authority | Product intent and design asset | Confirmed | User decision 2026-07-13; `../intake/V1_PACKAGE_INTAKE.md` receipt hashes | Supersedes the earlier repository product/UIUX interpretation | User |
| The delivery roadmap direction is V1.0 novel scenario, V1.1 AI content analysis and operations review, V1.2 AI content creation and operations closed-loop effect, then V2.0 stock/fund/futures research analysis and review | Product roadmap direction | Confirmed for ordering and named direction only | User messages 2026-08-12 in the current FlowVerse technical-solution conversation | Exact per-release scope, UIUX scenario allocation, acceptance, financial-domain behavior, and technical design remain subject to the review change set below | User |
| The current review may synchronize the repository PRD amendment, product/acceptance/implementation-plan summaries, versioned UIUX guidance, technical proposal, and system-decision Prompt proposal, followed by one overall review | Documentation change authorization | Confirmed for in-repository drafting/review only | User request in the current conversation, 2026-08-13; `../intake/V1_PACKAGE_INTAKE.md` scope `FV1-ROADMAP-REVIEW` | Does not approve the drafted content, modify the external package, accept an ADR, or release business implementation | User |
| The adversarial findings may be used to complete the repository PRD amendment, UIUX/acceptance overlays, detailed technical design, Proposed ADRs and delivery gates, followed by another overall review | Documentation completion authorization | Confirmed for in-repository drafting/review only | User requests 2026-08-15/16; `../intake/V1_PACKAGE_INTAKE.md` scope `FV1-DOCUMENT-COMPLETION`; `../engineering/V1_TECHNICAL_SOLUTION_ADVERSARIAL_REVIEW.md` | Does not approve the resulting product/UIUX/architecture contract, alter the external PRD/ZIP, authorize business code/dependencies/deployment, or prove HA/performance/recovery | User |
| The V1 roadmap/decision PRD amendment and its synchronized repository product, acceptance, implementation-plan, UIUX, high-level/detailed technical-solution, system-decision-Prompt, engineering-registry, Proposed-ADR and review documents form one proposed change set | Product/design/engineering review package | Proposed / IN_REVIEW; document reviews are advisory | `../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md`; `../product/PRODUCT_POSITIONING.md`; `../product/V1_PRODUCT_BRIEF.md`; `../uiux/ACCEPTANCE_CRITERIA.md`; `../uiux/UIUX_PRINCIPLES.md`; `../uiux/INTERACTION_RULES.md`; `../uiux/COPY_RULES.md`; `../uiux/DESIGN_TOKENS.md`; `../uiux/RELEASE_CAPABILITY_MATRIX.md`; `../uiux/SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md`; `../tasks/V1_IMPLEMENTATION_PLAN.md`; `../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md`; `../engineering/V1_DETAILED_TECHNICAL_DESIGN.md`; `../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`; `../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`; `../engineering/V1_FRONTEND_TECHNICAL_DESIGN.md`; `../engineering/V1_TECHNICAL_SOLUTION_EVALUATION.md`; `../engineering/V1_TECHNICAL_SOLUTION_ADVERSARIAL_REVIEW.md`; `../engineering/ARCHITECTURE_BASELINE.md`; `../engineering/RELIABILITY_BUDGET.md`; `../engineering/PERFORMANCE_BUDGET.md`; `../ai/SYSTEM_DECISION_PROMPTS.md`; existing ADR-0011～0024/0029/0030 files and `../decisions/DECISION_LOG.md` | Document findings may be closed by synchronized wording, but applicable ADR acceptance and explicit human approval remain required. No document in this set proves implementation, visual/behavior acceptance, Prompt effect, HA, recovery or performance | User / product / design / architecture owners |
| V1 validates one default user, one real novel, one real platform, and two consecutive valid Cycles | Product scope | Confirmed | PRD v1.1 sections 7.1 and 8.8 D045-D046 | Does not prove market value or causality | User / PRD |
| AI output remains candidate until a user confirms the corresponding formal record | Expected behavior | Confirmed | PRD v1.1 sections 3.8-3.18, 7.11, and 8.8 D017-D021 | None for product scope; persistence implementation is Unknown | User / PRD |
| Free Agent creation, arbitrary wiring, custom DAGs, and a general Workflow Builder are out of scope | Product boundary | Confirmed | PRD v1.1 section 7.2; UIUX `DesignSpec/workflow.md` section 1 | A read-only Agent execution trace remains in scope | User / package |
| React 19.2.7 and TypeScript 5.9.3 are approved only for the implemented diagnostic Web bootstrap | Target stack | Confirmed | User-approved bootstrap versions and completion instruction; ADR-0005; `../engineering/TECH_STACK.md`; `../../services/web/package.json`; lockfile | This does not authorize a product router, editor, component library or business UI dependency | User |
| UIUX package self-validation proves repository readiness | Validation result | Conflict | UIUX `DesignSpec/validation-report.json`: status `passed`, while multiple passed checks say `required ... missing` or `... not found` | Must be independently verified after controlled extraction/bootstrap | User / delivery team |
| V1 bootstrap uses separate `services/web`, `services/api`, and `services/worker` code/deployment directories | Approved architecture decision | Confirmed | User instruction 2026-07-15; `../decisions/ADR-0002-service-directory-topology.md`; checked-in manifests, locks, Dockerfiles and architecture check | This supersedes the shared API/Worker codebase in ADR-0001; it does not authorize further business microservices | User |
| The bootstrap uses the exact version pins and commands in TECH_STACK.md | Approved target stack, version, or command | Confirmed | User bootstrap approvals and diagnostic completion instruction; service manifests/locks; ADR-0002 and ADR-0005 | Host default Node remains older than the confirmed runtime; use Node 24.17.0 | User |
| PostgreSQL remains the only state dependency in the bootstrap service chain; a separate local diagnostic may authenticate PostgreSQL, Redis and MinIO without creating a business consumer | Approved architecture decisions | Confirmed | User approvals 2026-07-14/15/22/29; ADR-0002, ADR-0007 and ADR-0010; application/local deployment source | Business schema, retention, cache/object-storage contracts and least-privilege application accounts remain deferred | User |
| The services expose only operational diagnostic HTTP endpoints and contain no business API | Approved architecture decision | Confirmed | ADR-0002 and ADR-0005; API/Worker contract tests; Web parser tests | Public API adds `GET /api/v1/system/chain`; Worker status remains internal; response compatibility begins with checked-in tests | User |
| Local test deployment uses three native service processes through one PowerShell wrapper and no Docker/cloud control plane; CI/CD, test-server and production deployment targets are Unknown | Approved architecture decision | Confirmed repository implementation; production execution Unverified | User instruction 2026-07-21; ADR-0006; `../../deploy/local/start.ps1`; `../../scripts/start-local.ps1` | Earlier cloud-delivery decisions are superseded; selecting any remote target requires new approval and evidence | User / platform owner |
| Native local development may reach and authenticate the approved server middleware through loopback-only Windows OpenSSH forwarding and a non-business diagnostic | Approved development-access contract | Confirmed repository implementation; credentialed live result Unverified | User instructions 2026-07-24/29; ADR-0010; local tunnel/configuration/check source and tests | This does not approve public binds, firewall/security-group changes, SSH credential storage or business Redis/MinIO consumers | User / platform owner |
| The server middleware target is one three-container Compose project containing PostgreSQL 18.4 with pgvector 0.8.5 and TimescaleDB 2.28.3 OSS, Redis 8.8.0 and source-built MinIO `RELEASE.2025-10-15T17-29-55Z`; its one-command bootstrap creates only missing untracked secrets, its lightweight defaults keep internal memory below container limits, its MinIO builder downloads and builds one fixed canonical module through a configurable checksum-verified proxy without VCS/direct fallback, Redis preserves root-only secret files while its server process runs as `redis`, and no secret values or automatic extension/schema creation are committed | Approved deployment, extension, capacity and build-transport decisions | Confirmed repository configuration and script syntax; one target-server image-build and three-healthy-container smoke Confirmed | User instructions, target-server failure/build/health output 2026-07-22/23; ADR-0007/0008/0009; `../../deploy/server/middleware/` | SQL extension availability, long-duration stability, workload capacity, storage enforcement, backups, TLS, monitoring, HA, application production deployment, schemas/consumers and public exposure remain Unverified or outside scope | User / platform owner |
| The diagnostic chain uses synchronous Web → API → Worker checks with independent API/Worker PostgreSQL probes | Approved operational contract | Confirmed | User completion instruction 2026-07-20; ADR-0005; source and tests under `../../services/` | It authorizes no business API, task queue, Redis, broker or AI-provider execution | User |

“From the project package” is not a sufficient citation. Name the file, page, frame, section, key, script, or line.

The external PRD/UIUX receipt, hashes, and approved 2026-07-13 baseline remain unchanged while the roadmap change set is `IN_REVIEW`. Until the whole change set is reviewed, applicable ADRs are accepted, and the user gives final approval, implementation gates continue to read only separately `APPROVED` intake scopes; draft wording cannot silently narrow, defer, or satisfy the approved full-V1 package contract.

## Conflict Protocol

1. Record the competing claims and exact evidence.
2. Stop only the affected implementation path.
3. Explain user-visible, contract, data, security, and performance impact.
4. Present safe options without silently selecting one.
5. Resume only after the user records a decision or supplies stronger evidence.

## Prohibited Fabrication

AI must not invent or assert without evidence:

- API paths, methods, fields, status codes, schemas, tables, indexes, or relationships
- Frameworks, dependencies, package managers, providers, models, or versions
- Scripts, shell commands, environment variable names, ports, deployment targets, or CI behavior
- Routes, components, directories, assets, fonts, copy, permissions, roles, or security rules
- Test results, logs, screenshots, bundle sizes, latency, memory, cost, or optimization claims

Examples must be labeled “Example — not project fact” and cannot authorize code. Do not create manifests, configs, mocks, APIs, directories, or fake data merely to make an assumption appear true.
