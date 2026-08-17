# FlowVerse V1 Product Brief

## Status and Authority

- `IN_REVIEW` for the 2026-08-13 roadmap delta; retained behavior continues to summarize PRD v1.1 and the FlowVerse Phase 1 UIUX MVP package approved in `../intake/V1_PACKAGE_INTAKE.md`.
- The user's 2026-08-12 roadmap direction partitions the approved complete V1 contract into cumulative V1.0, V1.1, and V1.2 releases. The exact partition is the review candidate controlled by `FV1-ROADMAP-REVIEW`; the external PRD remains authoritative for retained product behavior and the final V1.2 full-loop result until final whole-change-set approval.
- Product and design facts in the approved external artifacts take precedence when this summary is merely incomplete; an actual conflict still stops the affected path under `../governance/EVIDENCE_POLICY.md`.
- The PRD explicitly does not select architecture, APIs, schemas, services, algorithms, runtime, or deployment.
- Default UI language is Simplified Chinese; brand presentation is “流界 FlowVerse”.

## Goal and Validation Unit

Deliver a traceable novel-creation and real-operation loop:

> Stage 0 → initial formal creation → manual external release → real feedback → formal analysis → human decision → next actual change → next release.

MVP validation uses one default user, one real novel task, one real target platform, and two consecutive valid Cycles. Additional task records may support testing, but they do not establish portfolio capability. Two Cycles validate repeatability and individual value only, not causality, market fit, growth, signing, exposure, or revenue.

### Cumulative delivery releases

| Release | Entry | First complete outcome | Completion boundary |
|---|---|---|---|
| V1.0 — 小说场景 | New novel task | Confirm a `CreationBaseline`; create, Review, human-confirm, recover, compare, and export the first immutable formal novel content snapshot with governed initial AI candidates | M0-M1 capability; actual release, feedback, analysis, and Cycle are not V1.0 release dependencies |
| V1.1 — AI 内容分析与运营复盘 | A V1.0 formal content snapshot that becomes publishable after the V1.1 operation baseline, packaging, and release checks are confirmed | Confirm an `OperationValidationBaseline`; create packaging and a release plan; record one real manual external release, feedback, an AI analysis candidate, a user-confirmed formal analysis, and a formal human decision | One real valid Cycle is the outcome gate. Evidence shortage may lead only to continued observation or an explicitly invalid Cycle, never fabricated success |
| V1.2 — AI 内容创作与运营闭环效果 | A current formal `HumanDecision` eligible to drive another iteration, plus an eligible task and frozen operation baseline; the next-round plan does not yet need to exist | Create and confirm the next-round plan, use the preceding valid Cycle N decision as traceable input to the next AI content or packaging candidates, confirm the actual change, release as adjacent Cycle N+1, compare the two consecutive valid Cycles, report individual value, and keep the following-Cycle path | M4-M7 and the full PRD 7.5/7.6 product contract; no causal, growth, market, or guaranteed-effect claim |

V1.0 includes AI-assisted first-version novel creation. “AI 内容创作” in V1.2 specifically means the later creation or packaging change driven by a confirmed operational decision. Release numbers never name content snapshots, packaging versions, or Cycle numbers, and every later release cumulatively regresses earlier due behavior.

## Release Safety, Availability, and Benchmark Boundary

Status: `IN_REVIEW / Proposed`. This section separates product-data safety from a deployment availability claim:

- `DataSafetyGate` is mandatory for H0. PostgreSQL-authoritative records, referenced objects and exports must form a consistent recoverable set with evidence for atomic/idempotent formal writes, backup/PITR, restore, deletion non-resurrection, readable history, and conservative degradation. Redis remains non-authoritative.
- `AvailabilityGate` requires a separate explicit human decision covering the target environment, measurement window, fault domain, capacity, monitoring, budget, and owner. The sole Confirmed availability number is the `99%` internal-MVP validation target, not a commercial SLA.
- `99.9%`, multi-AZ quorum/fencing, N-1 capacity, and replica counts remain `Proposed`. They neither block H0 product completion nor support an HA claim unless the `AvailabilityGate` is separately made applicable to that release and evidenced. Omitting that gate never waives `DataSafetyGate`.

The H0 benchmark fixture must use the external PRD's confirmed input boundaries: at most 20 files per task, 10 MB per file, 500,000 characters per file, 2,000,000 characters per task, and 300 pages for a text PDF. It also includes the default novel starting scope of a 20-chapter outline plus the first 3 chapters; that default remains user-adjustable in the Creation Baseline and is not another hard capacity limit.

Those values are workload inputs, not a performance result. H0 lab resources/environment, network, cold/warm state, concurrency/queue profile, sample count/noise, commands, and per-test warning/failure thresholds still require human approval; until then the performance gate remains `Unverified` even where a product-level response target is already Confirmed.

### Physical allowlist, horizontal gates, and completion evidence

The route/dialog detail remains synchronized with `../uiux/RELEASE_CAPABILITY_MATRIX.md`; a shell, deep link, Bot suggestion, or historical object cannot introduce a capability outside this allowlist.

| Gate | Physical allowlist | Horizontal gates | Required completion evidence |
|---|---|---|---|
| H0 / V1.0 | AUTH, P01, CreationBaseline Stage 0, P02, initial-creation P03; current-release Bot/Agent trace/pending/settings/activity; V1.0-scoped A01-A08 including A05; D01, D02 content, D03, D10, D11 content package | All V1.0 first-due AC/UIUX/Prompt assertions; identity/role, candidate/formal/human confirmation, compliance, responsive/mobile fail-closed, `DataSafetyGate`, export/delete/recovery, security, accessibility, and H0 benchmark. `AvailabilityGate` only when separately made applicable | Per-child/per-scenario evidence; allow/deny manifest; reconstructable, auditable, recoverable, comparable and exportable first formal snapshot; backup/restore/deletion drill; benchmark report with pending parameters visible; negative deep-link/action evidence |
| H1 / V1.1 | H0 plus OperationValidationBaseline Stage 0, P03 packaging handoff, P04, P05 analysis/decision; V1.1 A01-A08 extensions; D02 packaging, D04-D09, D11 review package, D12 cycle-time reconciliation | Full H0 regression plus V1.1 first-due and newly affected provider/Prompt/object/degradation/performance gates | Preserved H0 history; one real valid ActualRelease-to-feedback-to-formal-analysis-to-formal-decision Cycle; negative evidence that continue-observing/invalid Cycle does not complete H1; updated allow/deny manifest |
| H2 / V1.2 | H0/H1 plus P03 decision-driven creation, P05 next-round/comparison/value/following Cycle N+2; V1.2 A01-A08 extensions; D11 full-lineage package and D12 two-Cycle survey | Full H0/H1 regression plus every V1.2 first-due and complete cross-cutting gate | First adjacent valid Cycle N/N+1 lineage, comparison classification, individual-value result, following Cycle N+2 path, and row-level PRD 7.5/7.6, AC-01-35 and UIUX 1-130 evidence |

Not-introduced scope is explicit: H0 excludes P04/P05, V1.1 operational workloads, D04-D09/D12 and next-round/value controls; H1 still excludes decision-driven next-round creation, adjacent-Cycle comparison/value, and D12 two-Cycle survey; H2 still excludes all V2 financial routes, objects, data, and actions. Unknown or stale capability fails closed for mutation and AI execution while authorized history remains readable where its freshness can be stated.

### Human decision points before an applicable release gate

The product owner must explicitly settle: (1) PostgreSQL production writer/fault-domain and backup/PITR ownership; (2) object-store business account/bucket, TLS/encryption, lifecycle/version/delete and cross-store recovery boundary; (3) recovery data set, RTO/RPO exercise, owner, and deletion non-resurrection mechanism; (4) dependency-specific read-only/draft/formal-write/AI degradation and retry behavior; (5) H0 performance environment, concurrency, samples, commands and thresholds; and (6) whether a production `AvailabilityGate` is applicable beyond the Confirmed internal-MVP 99% target. Until the relevant decision is recorded, the affected gate is `Unverified`; current middleware health alone is not product-release evidence.

## Primary Product Contract

1. The work home combines the shared Bot, continue work, pending work, and the complete task list.
2. Bot and deterministic entry points operate on the same server-authoritative business state. Bot failure never blocks task navigation or structured forms.
3. In the novel scenario, one long-running task owns one novel; tasks isolate content, references, versions, executions, and Cycles.
4. AI outputs are candidates. Setting a primary candidate is not formal confirmation.
5. Formal content, work memory, packaging, release facts, feedback snapshots, formal analyses, and human decisions require the default user's explicit confirmation.
6. Every formal content confirmation creates a complete immutable snapshot. Retry, correction, replacement, and model switching create new records rather than overwriting history.
7. A normal Cycle begins only when a user confirms an actual external release as effective; that confirmation and Cycle creation are one atomic product action.
8. A valid Cycle closes normally only through a confirmed human decision after all validity conditions pass. “Continue observing” keeps it active.
9. One task has at most one active Cycle, and one user has at most one paid AI execution slot across lightweight Bot calls and business AI execution.
10. Administrators configure, monitor, and audit. They cannot impersonate the user, authorize AI on the user's behalf, or confirm user business facts.
11. Stage 0 is one cumulative product baseline with two separately confirmed parts: V1.0 `CreationBaseline` and V1.1 `OperationValidationBaseline`. Neither part may be inferred from AI output or silently backfilled.
12. A V1.0 task upgrades to V1.1 by explicitly confirming its operation baseline. The upgrade preserves the creation baseline and all existing formal history; it does not claim earlier content or executions used facts that were confirmed only later.

## Versioned Stage 0 Baseline

| Formal part | First due | Proposed allocated fields (source: PRD amendment §3) | Freeze and change rule |
|---|---|---|---|
| `CreationBaseline` | V1.0 | Task name; creative idea and optional must-keep/avoid/existing elements; genre, target reader, and task/creation goal; initial outline/first-chapter scope, its business completion criteria, and language strength; Review configuration; model pool, default candidate count, and applicable creation budget; reference-rights declaration plus allowed-content boundary (explicit N/A when no reference). Internal release status is not a user baseline field | User-confirm before the first formal creation batch. A change creates a traceable replacement and revalidates affected candidates, Review, memory, and formal-content dependencies; it never rewrites existing snapshots |
| `OperationValidationBaseline` | V1.1 | One target platform and account identifier; formal content/packaging release scope; metric definitions, unit, cumulative/interval basis, timezone, formal observation points and data-completeness requirement; Cycle budget; two-valid-Cycle validation goal, comparison limits and prohibited claims; manual coordination-time baseline or explicit “no reliable baseline”. Task-level AI budget and per-execution ceiling are referenced from the separate budget policy, not duplicated as drifting baseline fields | User-confirm before a release plan can become ready for actual release. Platform, metric, time, and validation fields remain frozen through the formal decision of the latter Cycle in the candidate adjacent valid pair N/N+1. Before the first Cycle, a change requires impact preview/replacement confirmation; once validation has started, a material change interrupts the prior run and restarts the consecutive-valid baseline without rewriting occurred Cycle numbers |

The V1.1 operation part extends the same task baseline; it is not a second task or an AI-generated default. UI copy may continue to say “阶段 0”, but it must identify which part is confirmed, missing, replaced, or blocking the current release capability.

The server exposes distinct `creationReady` and `operationReady` semantics: the former requires only the confirmed CreationBaseline for V1.0 creation, while the latter requires both baseline parts for V1.1 release/Cycle work. An unqualified Stage-0-complete flag is forbidden.

`CreationBaseline` owns the initial-batch constraints and initial defaults. Advanced Settings may version only future-execution preferences inside the confirmed model, language, budget, and rights boundaries; D01 and each `ExecutionBinding` freeze the actual values used. Expanding a formal boundary requires a replacement baseline and impact propagation, while changing an in-bound future preference does not rewrite the baseline. Per-reference provenance, rights, and actual-use records remain mandatory even when the baseline declares an overall rights boundary.

## MVP Capability Scope

| ID | Capability | Required product result | First due release |
|---|---|---|---|
| C01 | Accounts and permissions | One default user and one administrator, first-login password change, lockout, session expiry, and hard role isolation | V1.0 |
| C02 | Work home and tasks | Shared Bot plus deterministic start/continue/pending/task-list entry points, with independent degradation | V1.0 |
| C03 | Stage 0 | Confirm `CreationBaseline`, then cumulatively extend it with `OperationValidationBaseline` before release/Cycle work | V1.0 / V1.1 |
| C04 | Task cockpit | Show lifecycle, control, visibility, deletion, blockers, current Cycle when applicable, budget, and exactly one primary next action | V1.0; Cycle states V1.1 |
| C05 | Creative references | Text/TXT/Markdown/DOCX and optional text PDF with rights, provenance, selected fragments, actual use, and deletion impact | V1.0 |
| C06 | Novel creation | Story settings, characters, outline, first chapters, later edits, candidates, Review, and formal snapshots | Initial creation V1.0; decision-driven next change V1.2 |
| C07-C08 | Agent/model execution | Role-based collaboration, model/provider separation, preview, queue, attempts, partial failure, retry, cost, and budget | V1.0; each later workload requalifies |
| C09-C10 | Review, memory, versions | Candidate/formal separation, six Review dimensions, disagreements, memory changes, immutable snapshot comparison | V1.0 |
| C11-C14 | Release and Cycle | Packaging, release plan, actual release, external events, feedback, formal analysis, human decision, next-round change, and Cycle N | Single-Cycle review V1.1; successive closed loop V1.2 |
| C15 | Global assistance | One Bot capability, Agent collaboration, pending, settings drawers, and an activity popover with non-overlapping duties | V1.0, extended per release |
| C16-C18 | Governance | Compliance/copyright/AI labels/provider policy, export/deletion, configuration, monitoring, and audit | Due controls in every release; cumulative completion V1.2 |

## Page and Surface Scope

- Authentication: login, first password change, lockout, and session recovery.
- P01: work home with Bot, continue work, pending summary, and task list.
- Stage 0: V1.0 creation-baseline flow plus the V1.1 operation-validation extension; each part has an explicit formal state.
- P02: task cockpit.
- P03: creation workbench for references, settings, characters, outline, chapters, candidates, Review, memory, and versions.
- P04: release and observation, first enabled in V1.1.
- P05: review and decision, first enabled in V1.1 and extended with Cycle comparison/value in V1.2.
- Auxiliary surfaces: shared Bot drawer, Agent collaboration, pending work, advanced settings, and activity.
- Administration: accounts, scenario/Agent configuration, model/cost, Prompt/Review rules, compliance/platform policies, monitoring, and audit.

## Experience and Device Rules

- Use a calm, low-saturation editorial-workbench visual system with one primary action per page state.
- Manuscript, evidence, versions, and next action take precedence over AI decoration or process graphics.
- Agent execution topology is a read-only trace. It may support pan, zoom, node inspection, and attempt recovery, but never arbitrary wiring or saved custom workflows.
- Baseline viewport is 1440 × 900; minimum desktop is 1280 × 720.
- At 390 × 844, login and simple questionnaire use may remain available, but work-home Bot input, complex editing, execution, formal confirmation, release, decision, task control, and admin remain read-only or disabled with an explanation.
- Every surface covers loading, empty, failure, stale, offline, blocked, unsaved, cancellation, and recovery states applicable to it.

## Explicitly Out of Scope

- Public registration, invitations, password recovery, MFA, SSO, multi-user teams, and enterprise roles.
- Automated platform login, release, withdrawal, scraping, or credential storage.
- Multi-platform experiments for one task; full existing-serial import; cross-task knowledge base; knowledge graph; OCR; web scraping; cloud sync; audio/video; fine-tuning; BYOK.
- Free Agent creation, arbitrary graph wiring, custom workflow/DAG saving, Agent/Prompt/template markets, and paragraph-level intelligent merge.
- AI auto-confirmation, automated human decision, full mobile creation/admin, or subscription/payment.
- Any second product scenario inside V1.0-V1.2. V2.0 is directed toward stock, fund, and futures research/analysis/review, but requires its own approved product, compliance, data, and acceptance baseline before implementation.

## Product Constraints on Architecture

- Formal records are immutable and traceable; corrections and replacements preserve predecessors.
- Actual-release confirmation and Cycle creation cannot expose an intermediate inconsistent state.
- Candidate, formal content, work memory, packaging, actual release, feedback, analysis, and decision are distinct ownership domains.
- Model/provider policy is evaluated for every execution; screenshots are never sent to models.
- Retry, model switching, partial completion, input/config/provider versions, and incurred cost remain auditable.
- Compliance blocking applies equally to user and administrator surfaces and has no bypass.
- Deletion, export, recovery, and administrator debug access must be demonstrably enforceable.

## Completion

- Each release passes its exact first-due assertions plus every earlier cumulative assertion in `../uiux/ACCEPTANCE_CRITERIA.md`; an unsplit parent AC cannot be called Passed from only one child assertion.
- V1.0 completion proves first-version novel creation and its horizontal trust/UIUX/governance gates, including mandatory `DataSafetyGate`, without claiming release/Cycle completion or unapproved production availability.
- V1.1 completion proves one real valid release-to-analysis-to-formal-human-decision Cycle; “continue observing” remains a non-decision and cannot satisfy that completion result.
- V1.2 completion passes AC-01 through AC-35, the exact product matrix in PRD v1.1 section 7.5, every section 7.6 Cycle-validity item for the first adjacent valid Cycle pair N/N+1, and the following Cycle N+2 path (Cycle 3 on the normal 1→2 path).
- Required external platform, provider policy, model/version/price, deletion/recovery, and real-validation gates are confirmed at their stated checkpoints.
- Repository-defined engineering, accessibility, reliability, performance, security, and recovery checks pass when their tooling and targets are approved; unavailable checks remain Unverified.
