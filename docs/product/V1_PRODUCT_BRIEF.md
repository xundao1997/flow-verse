# FlowVerse V1 Product Brief

## Status and Authority

- Repository summary of PRD v1.1 and the FlowVerse Phase 1 UIUX MVP package approved in `../intake/V1_PACKAGE_INTAKE.md`.
- Product and design facts in the approved external artifacts take precedence over this summary when wording is incomplete; conflicts still follow `../governance/EVIDENCE_POLICY.md`.
- The PRD explicitly does not select architecture, APIs, schemas, services, algorithms, runtime, or deployment.
- Default UI language is Simplified Chinese; brand presentation is “流界 FlowVerse”.

## Goal and Validation Unit

Deliver a traceable novel-creation and real-operation loop:

> Stage 0 → initial formal creation → manual external release → real feedback → formal analysis → human decision → next actual change → next release.

MVP validation uses one default user, one real novel task, one real target platform, and two consecutive valid Cycles. Additional task records may support testing, but they do not establish portfolio capability. Two Cycles validate repeatability and individual value only, not causality, market fit, growth, signing, exposure, or revenue.

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

## MVP Capability Scope

| ID | Capability | Required product result |
|---|---|---|
| C01 | Accounts and permissions | One default user and one administrator, first-login password change, lockout, session expiry, and hard role isolation |
| C02 | Work home and tasks | Shared Bot plus deterministic start/continue/pending/task-list entry points, with independent degradation |
| C03 | Stage 0 | Freeze creative start, target platform, scope, indicators, observation points, models, budget, language, and validation goal |
| C04 | Task cockpit | Show lifecycle, control, visibility, deletion, blockers, current Cycle, budget, and exactly one primary next action |
| C05 | Creative references | Text/TXT/Markdown/DOCX and optional text PDF with rights, provenance, selected fragments, actual use, and deletion impact |
| C06 | Novel creation | Story settings, characters, outline, first chapters, later edits, candidates, Review, and formal snapshots |
| C07-C08 | Agent/model execution | Role-based collaboration, model/provider separation, preview, queue, attempts, partial failure, retry, cost, and budget |
| C09-C10 | Review, memory, versions | Candidate/formal separation, six Review dimensions, disagreements, memory changes, immutable snapshot comparison |
| C11-C14 | Release and Cycle | Packaging, release plan, actual release, external events, feedback, formal analysis, human decision, and Cycle N |
| C15 | Global assistance | One Bot capability, Agent collaboration, pending, settings drawers, and an activity popover with non-overlapping duties |
| C16-C18 | Governance | Compliance/copyright/AI labels/provider policy, export/deletion, configuration, monitoring, and audit |

## Page and Surface Scope

- Authentication: login, first password change, lockout, and session recovery.
- P01: work home with Bot, continue work, pending summary, and task list.
- Stage 0: six-step creation and validation baseline flow.
- P02: task cockpit.
- P03: creation workbench for references, settings, characters, outline, chapters, candidates, Review, memory, and versions.
- P04: release and observation.
- P05: review and decision.
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
- AI auto-confirmation, automated human decision, full mobile creation/admin, subscription/payment, or a second product scenario.

## Product Constraints on Architecture

- Formal records are immutable and traceable; corrections and replacements preserve predecessors.
- Actual-release confirmation and Cycle creation cannot expose an intermediate inconsistent state.
- Candidate, formal content, work memory, packaging, actual release, feedback, analysis, and decision are distinct ownership domains.
- Model/provider policy is evaluated for every execution; screenshots are never sent to models.
- Retry, model switching, partial completion, input/config/provider versions, and incurred cost remain auditable.
- Compliance blocking applies equally to user and administrator surfaces and has no bypass.
- Deletion, export, recovery, and administrator debug access must be demonstrably enforceable.

## Completion

- All applicable requirements in `../uiux/ACCEPTANCE_CRITERIA.md` pass with evidence.
- The exact product matrix in PRD v1.1 section 7.5 and Cycle validity checklist in section 7.6 pass.
- Required external platform, provider policy, model/version/price, deletion/recovery, and real-validation gates are confirmed at their stated checkpoints.
- Repository-defined engineering, accessibility, reliability, performance, security, and recovery checks pass when their tooling and targets are approved; unavailable checks remain Unverified.
