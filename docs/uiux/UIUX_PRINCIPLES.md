# FlowVerse UIUX Principles

## Authority and Direction

The approved direction is an **editorial workbench with restrained AI presence**: warm, calm, traceable, recovery-oriented, and suitable for long-form writing. Exact contracts and visual references come from the UIUX package identified in `../intake/V1_PACKAGE_INTAKE.md`.

The external package remains unchanged evidence. The following roadmap delta is a proposed, `IN_REVIEW` repository UIUX conflict resolution and phased-release overlay; it does not amend the approved package or authorize implementation until the whole review set receives explicit human approval. In particular, the proposal resolves the package's isolated D10 mobile-resume exception by disabling every D10 task-control mutation at mobile read-only width. Proposed additions for decision candidates, controlled Prompt governance, and release capability require approval and new evidence; package screenshots do not prove those states. `RELEASE_CAPABILITY_MATRIX.md` is the proposed UI capability and route companion to these principles.

## Product Hierarchy

1. Current formal content, evidence, and business state.
2. The single next action allowed by the current state.
3. Candidate differences, decision candidates with evidence, Review findings, and user decisions.
4. Actual Agent/model participation, execution progress, cost, and recovery.
5. Supporting navigation, settings, activity, and system status.

AI appearance must come from process transparency, provenance, and precise feedback. It must not crowd out manuscripts, formal records, or evidence.

## Work Home

- P01 is the work home, not a marketing page, isolated task list, or generic chatbot homepage.
- Keep the shared Bot, continue work, pending summary, and complete task list visible as independent regions.
- Natural-language and deterministic entry points operate on the same business state and remain usable independently.
- Bot replies and action cards are separate. No navigation, draft write, task creation, business execution, or formal mutation occurs until the user activates the explicit action.
- Ambiguous task, Cycle, object, or action context requires a visible choice; never silently select the most recent item.

## Creation and Formality

- Manuscript and formal content receive the largest, quietest usable area.
- Visually distinguish candidate, primary candidate, accepted risk, formal content, observation, analysis, recommendation, and human decision.
- A primary candidate always retains “尚未正式确认” until formal confirmation succeeds.
- Formal mutations use specific confirmation copy, show object/version/impact, reject duplicate submission, and wait for authoritative success.
- Historical snapshots, attempts, corrections, and decisions are read-only and never visually imply overwrite.

## Decision Candidates and Human Authority

- Deterministic state and capability remain authoritative. If the system can resolve one legal next action without semantic judgment, that action remains the page's only primary action and no model recommendation replaces it.
- S-layer semantic output is an untrusted `SemanticFindingCandidate`, rendered only in a `DecisionCandidatePanel` on the business page that owns the decision. It is not a new global workspace, a formal fact, or permission to mutate state.
- The panel always shows candidate status, the question being considered, input/object versions, supporting evidence, challenging evidence, contradictions, missing evidence, risk flags, alternatives, and whether human review is required. Evidence links identify source, version, locator, and relation to the claim.
- The model-originated status is limited to `candidate`, `abstain`, or `needs_human_review`. Invalid schema/evidence, unknown labels, stale input, deterministic hard gates, or compliance policy may add a separate authoritative validation/policy-block state. The UI names that owner and reason; it never says the model candidate decided `BLOCK`.
- `abstain`, `needs_human_review`, or any authoritative invalid/blocked state never maps to an executable recommendation. The UI preserves safe inspection where authorized, explains the next recovery, and disables adoption.
- When several legal low-risk actions remain, the sole primary action is to review or choose among those options. A selected option becomes a formal action only after the owning page revalidates capability and presents its normal confirmation path.
- Mobile read-only may display the panel and evidence, but it cannot apply a field, select an action for execution, accept risk, complete human review, or perform formal confirmation.

## Agent and Workflow Visualization

- Show only actually activated business roles and actual model participation.
- Agent execution is a read-only trace with inputs, handoffs, versions, attempts, partial results, cost, failures, and user checkpoints.
- Do not expose free Agent creation, Prompt editing, arbitrary wiring, topology mutation, custom DAG persistence, or a general Workflow Builder.
- Agent detail supports understanding and recovery; it is not an independent chat surface or first-level product area.

## Controlled Prompt Governance

- A05 is an administrator-only registry, evaluation, promotion, revoke, and rollback surface. It is not an online free-form Prompt editor, playground, toolbox, marketplace, or general rule engine.
- Production A05 shows immutable Prompt family/version plus `PromptConfigBundle`, `EvaluationBinding`, and safe `ExecutionBinding` identities/hashes, applicable product release/workload, evaluation evidence, actor separation, activation history, current champion, and a last-known-good association only when one exists. It never exposes secrets, raw protected inputs, or hidden holdout contents.
- Automated checks may advance only to `OfflinePassed`. Human approval and production activation are explicit, separately authorized actions; a score, model judge, usage metric, or model-reported confidence can never auto-promote a version.
- Promotion, activation, emergency revoke, and rollback show version, environment/scope, evidence status, affected new/queued/running execution behavior, reason, actor, revision, and audit receipt. Missing or stale evaluation evidence fails closed.
- The visible lifecycle is `Draft → Candidate → OfflinePassed → HumanApproved → ExplicitPilot/Shadow → ControlledCanary → Active → Deprecated/Revoked/RolledBack`. A first version has no fabricated rollback target: its controlled launch uses `ExplicitPilot`, and a stop condition disables the affected AI capability and routes to the deterministic/manual flow. Only a later version with a verified last-known-good can offer rollback.
- A change author cannot be the sole reviewer and activator for the same version. If the approved account/permission model cannot prove the required separation, the activation action remains disabled rather than weakening the gate.
- A05 is unavailable on mobile. At compact-workspace width its evidence and version comparison reflow into labeled details or one exclusive overlay without dropping hidden columns or approval reasons.

## Primary Action and States

- Exactly one action receives primary visual emphasis in each page state.
- Disabled formal actions remain discoverable and explain every blocking reason and recovery path.
- Loading, empty, failure, stale, offline, partial, budget, policy, compliance, unsaved, and cancellation states preserve valid content and deterministic navigation.
- Progress shows real stage, updated time, completed outputs, and cost; never fabricate a percentage.

## Reading, Responsive, and Accessibility

- Baseline: 1440 × 900. Minimum desktop: 1280 × 720.
- At 1440 and wider, keep the writing surface dominant and contextual regions secondary.
- At 1280–1439, preserve the desktop information hierarchy while converting fixed secondary context into an overlay before reducing manuscript usability.
- At 768–1279, use the compact-workspace layout. Authorized desktop business capabilities normally remain available while navigation, evidence, comparison, tables, drawers, and dialogs reflow into a single readable column or exclusive full-height overlay. Formal state and the one primary action cannot be hidden, clipped, or placed behind hover-only interaction. If the actual viewport/input environment cannot safely present the complete formal preview and confirmation, that exact action fails closed with an explicit requirement to continue in an approved environment of at least 1280 × 720; compact width never silently drops fields or submits a reduced confirmation.
- At 767 and narrower, including the 390 × 844 reference, preserve readable task/status/formal content and read-only decision evidence. Disable complex creation, Bot input/action execution, formal confirmation, release, decision, every D10 task-control mode including resume, and admin with “请使用桌面端继续此操作”. D11 approved-package preview/download and D12 simple survey remain the only package-defined mobile exceptions and do not broaden any other capability.
- Maintain keyboard navigation, visible focus, semantic landmarks, focus return, error association, reduced motion, and non-color state cues.

## Avoid

- Sci-fi dashboards, neon graphs, animated data-flow spectacle, dense KPI walls, or decoration competing with text.
- Treating AI output, Agent summaries, or administrator actions as user-confirmed fact.
- Treating a `SemanticFindingCandidate`, any future calibrated hint, or a recommended action as an authoritative next action, human decision, or executable command, or presenting a deterministic/compliance block as a model decision.
- Exposing raw Prompt editing in production A05 or allowing evaluation scores to promote a Prompt automatically.
- Showing a later-release route or action as usable when its release capability is absent, unknown, or stale.
- Hiding formal state or the primary action at 1280 desktop width.
- Multiple peer primary actions, invisible disabled reasons, destructive ambiguity, or silent optimistic formal updates.
