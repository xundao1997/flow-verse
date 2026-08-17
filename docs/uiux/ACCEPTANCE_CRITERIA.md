# FlowVerse V1.0-V1.2 Acceptance Criteria

## Authority and Release Identity

- Roadmap-delta status: `IN_REVIEW / Proposed`. The release split, child assertions, and added evidence gates below cannot authorize implementation or claim acceptance before explicit overall human approval.
- These repository IDs summarize the approved PRD v1.1 sections 7.5-7.10 and UIUX `DesignSpec/state_matrix.json` scenarios 1-130.
- The PRD matrix and Cycle validity checklist remain authoritative when this summary is less specific.
- The user's approved 2026-08-12 roadmap direction names the V1.0, V1.1, and V1.2 order and themes. This `IN_REVIEW` overlay proposes the cumulative release gates and first-due allocation below without changing the final complete-V1 product result.
- V1.0 is the first implemented product release; earlier direction-document provenance creates no migration or compatibility acceptance.
- The package's 130 scenarios remain the complete V1 superset inventory; they are not implicitly partitioned by numeric range. The unchanged package remains evidence; this `IN_REVIEW` overlay proposes resolving the D10 responsive conflict by disabling every D10 task-control mutation at `0–767px`, including resume.
- New decision-candidate, controlled Prompt-governance, release-capability, compact-workspace, and system-degradation/recovery states are proposed and `IN_REVIEW`; after approval they require new exact UIUX evidence, because existing package screenshots do not prove them.

## Release Applicability and Cumulative Gate

- `First due` means the assertion must pass before that release can ship. V1.1 must regress all V1.0 assertions; V1.2 must regress all V1.0 and V1.1 assertions.
- The proposed `IN_REVIEW` release-capability matrix assigns every route, subpage, surface, state, action, scenario, and AC as introduced, required, regression-only, or N/A with reason. If approved, normal navigation, direct links, Bot/action cards, pending/activity entries, exports, and administrator navigation must consume the same server-authoritative capability result and UI matrix semantics.
- A capability absent from the current release is absent from normal navigation. A direct or stale deep link shows an explicit current-release unavailable state and safe return path; unknown or stale capability fails closed for writes and AI execution.
- A release gate records each due child assertion independently. A split top-level parent remains `Partially qualified / Unverified`—never Passed—until every child in its complete V1.2 scope has exact evidence; passing all children due through V1.0 or V1.1 proves that release's scoped gate only, not the unsplit parent.
- AC-24 through AC-30 and AC-35 are horizontal release gates for every version and apply again to every newly enabled surface. Proposed child assertion AC-24A carries the release-capability consistency gate, while AC-26A/26B/26C carry the H0/H1/H2 degradation-and-recovery qualification, without changing the approved top-level AC-01 through AC-35 inventory.
- V1.0 and V1.1 may pass their own scoped release gates without claiming the approved PRD's complete two-Cycle MVP. Only V1.2 may claim complete V1 acceptance, after all AC-01 through AC-35, PRD 7.5, PRD 7.6, and applicable UIUX scenarios pass.

| Release | First complete outcome | New assertions first due | Cumulative outcome gate |
|---|---|---|---|
| V1.0 — 小说场景 | Human-confirmed first formal novel snapshot from governed initial AI candidates and a confirmed `CreationBaseline`; creation recovery, comparison, content export, and horizontal trust controls work | AC-01-05, AC-06A, AC-07, AC-08A/AC-08C, AC-09A, AC-10-11, AC-18, AC-19A, AC-20/20A/20B through AC-23, AC-24/24A, AC-25, AC-26/26A, AC-27-31, AC-32A, AC-33A, AC-34A, AC-35 | M0-M1 capability; no actual release or Cycle evidence is claimed |
| V1.1 — AI 内容分析与运营复盘 | A confirmed `OperationValidationBaseline`, real manual release, valid evidence/feedback, AI analysis candidate, user-confirmed formal analysis, and a formal human decision for one valid Cycle | AC-06B, AC-08B, AC-09B, AC-12-15, AC-19B, AC-26B, AC-32B, AC-33B, AC-34B, plus the horizontal gates on P04/P05 | One real valid Cycle; insufficient evidence may only continue observation or end explicitly invalid |
| V1.2 — AI 内容创作与运营闭环效果 | A current formal human decision drives the next actual AI-assisted content/packaging change and adjacent valid release; Cycle N/N+1, comparison, value result, and following Cycle N+2 path exist | AC-16-17, AC-19C, AC-26C, AC-32C, AC-33C, AC-34C, plus full closure of every parent/child assertion | All AC-01-35 including due child assertions, PRD 7.5/7.6, the first adjacent pair of real valid Cycles, and applicable UIUX scenario evidence |

### Child assertions for cross-release ACs

| Parent | Child assertion | Required result |
|---|---|---|
| AC-06 | AC-06A — V1.0 | The user confirms and freezes every `CreationBaseline` field defined by `../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md` section 3.1, including task/creative inputs, first-content scope and business completion criteria, language, Review, model/candidate/budget choices, and reference-rights boundary. Internal release status is never requested as a business field. Changes create traceable replacements and revalidate affected creation dependencies without rewriting formal snapshots |
| AC-06 | AC-06B — V1.1 | Before a release plan can become ready, the user confirms every `OperationValidationBaseline` field defined by the PRD amendment section 3.2, including platform/account/release scope, metric/time/completeness, Cycle budget, validation/comparison/claim limits, and manual-time baseline state. Task AI budget remains a referenced separate policy. The extension never rewrites AC-06A; a change before any Cycle requires impact preview/reconfirmation, while a material change after validation starts also restarts the consecutive-validation baseline without rewriting occurred Cycle numbers |
| AC-08 | AC-08A — V1.0 | Candidate, primary candidate, human-edited candidate, accepted risk, formal content, and work memory are visibly and behaviorally distinct |
| AC-08 | AC-08B — V1.1 | Observation, analysis candidate, formal analysis, recommendation, continue-observing action, and formal human decision are visibly and behaviorally distinct |
| AC-08 | AC-08C — Decision candidate | Every `SemanticFindingCandidate` remains visibly non-authoritative in `DecisionCandidatePanel` and shows question/version, evidence references, counterevidence, contradictions, missing evidence, risks, alternatives, status, and human-review need. Model status is limited to `candidate`, `abstain`, or `needs_human_review`; validator/compliance blocks are separately attributed. Every abstain, review-required, invalid, blocked, or stale result is non-adoptable and exposes a safe recovery path |
| AC-09 | AC-09A — V1.0 | Formal content and work-memory records require the default user's explicit confirmation; AI output or primary-candidate selection never formalizes them |
| AC-09 | AC-09B — V1.1 | Packaging, actual release facts, feedback snapshots, formal analysis, and human decisions each require their owning user confirmation; no upstream confirmation silently confirms a downstream object |
| AC-19 | AC-19A — V1.0 | Main-editor/coordinator, chapter-creation, and editor-review roles produce real stage-appropriate outputs and handoffs; at least two approved provider families independently produce candidates from the same brief |
| AC-19 | AC-19B — V1.1 | The operations-analysis role produces the analysis candidate from bound evidence; cumulatively all three approved provider families have participated, with the third used for independent review or another eligible key execution |
| AC-19 | AC-19C — V1.2 | The revision-director role converts a formal human decision into a bounded next-round plan. The five required core novel roles and all three provider families now satisfy the complete PRD evidence contract; irrelevant roles never appear merely to satisfy a count |
| AC-26 | AC-26A — H0 / V1.0 | Every H0 surface implements the common [system degradation and recovery contract](SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md): `degradationMode`, `affectedCapabilities`, `dataFreshness`/`asOf`, `retryable`/`retryAfter`, and optional verified `lastKnownGoodRef` remain consistent; draft save, formal write, read-only query, AI candidate, and object operations follow their distinct fail-open/fail-closed rules; 429/503 recovery is bounded; one CTA, mobile read-only, preserved input, and accessible status all pass |
| AC-26 | AC-26B — H1 / V1.1 | AC-26A fully regresses on H0 and extends to P04/P05, release/external facts, feedback, analysis, human decision, export, and Cycle reconciliation. Stale or unknown external evidence cannot authorize an actual release, formal analysis, or human decision, and partial dependency failure preserves unaffected V1.0 work |
| AC-26 | AC-26C — H2 / V1.2 | AC-26A/26B fully regress and extend to the decision-driven next round, N/N+1 comparison/value, following Cycle N+2, complete export, and the D12 simple survey. Stale prior-Cycle facts are visibly dated and cannot drive a new formal action; mobile degradation never widens its approved exception |
| AC-32 | AC-32A — V1.0 | The content export binds an exact formal content snapshot and preserves due AI/reference declarations |
| AC-32 | AC-32B — V1.1 | The operational review export binds the exact release, evidence, feedback snapshots, formal analysis, and human action |
| AC-32 | AC-32C — V1.2 | The complete task export preserves the decision-to-change-to-release lineage, Cycle comparison, value result, and all required declarations |
| AC-33 | AC-33A — V1.0 | Pause, terminate, archive, delete, recovery, and retention work for task/creation history without inventing Cycle effects |
| AC-33 | AC-33B — V1.1 | Task controls and release/feedback correction preserve the active Cycle, invalidation, replacement, and retention rules |
| AC-33 | AC-33C — V1.2 | Successive-Cycle history, upgrade, restore, and recovery preserve cumulative lineage and never rewrite an earlier release's formal facts |
| AC-34 | AC-34A — V1.0 | Identity, novel-role, model/provider, Prompt/Review, compliance, and creation-related configuration is versioned and auditable for V1.0 execution |
| AC-34 | AC-34B — V1.1 | Platform, metric, feedback-analysis, and operations-review configuration follows the same new-execution-only and historical-association rules |
| AC-34 | AC-34C — V1.2 | Decision-driven creation and Cycle-comparison configuration remains bound through execution, version, release, analysis, and audit lineage |

D12 is split by mode: `cycleTimeReconciliation` is first due in V1.1 after every ended Cycle, including the Cycle N that may later become the first member of a valid adjacent pair, on desktop/compact workspace; `twoCycleSurvey` is first due in V1.2 after Cycle N+1 and is the only D12 mobile-write exception.

## Product and Trust — Must Pass

- [ ] AC-01: The default user and administrator complete first-login password change, lockout, session expiry, and hard role isolation; administrators cannot impersonate users or confirm user business facts.
- [ ] AC-02: P01 presents the shared Bot, continue work, pending summary, and complete task list as independent regions; model/Bot failure does not block deterministic entry.
- [ ] AC-03: Bot context always identifies global/task/Cycle/object scope; ambiguity requires an explicit mutually exclusive choice and task switching does not leak writable context.
- [ ] AC-04: Bot text alone changes no task, draft, Cycle, formal object, or execution. Action cards revalidate target/revision/policy/budget before any permitted action.
- [ ] AC-05: Business AI requests route to the owning page and execution preview; formal and dangerous actions route to their owning page and cannot be confirmed from the work home or drawer.
- [ ] AC-06: Stage 0 exposes two authoritative readiness states. `creationReady` requires AC-06A/`CreationBaseline` and enables V1.0 creation; `operationReady` requires both AC-06A and AC-06B/`OperationValidationBaseline` and enables V1.1 release/Cycle work. UI and capability code must not use an unqualified “Stage 0 complete” flag that lets missing V1.1 fields block V1.0 or lets creation readiness authorize release.
- [ ] AC-06 configuration ownership: `CreationBaseline` freezes initial-batch constraints/defaults; Advanced Settings may change only future preferences inside those boundaries; D01/`ExecutionBinding` freezes actual execution values. Expanding model/language/budget/rights boundaries requires a replacement baseline and dependency revalidation, and an overall rights boundary never replaces per-reference provenance and permission checks.
- [ ] AC-07: One novel task isolates its content, references, executions, versions, releases, feedback, and Cycles from every other task.
- [ ] AC-08: The object distinctions in AC-08A through AC-08C remain visible and behavioral; a label-only distinction does not pass.
- [ ] AC-09: The confirmation boundaries in AC-09A and AC-09B hold; AI output never becomes formal implicitly.
- [ ] AC-10: Every formal content confirmation creates an immutable complete snapshot; retry, model switching, correction, and replacement preserve prior records and costs.
- [ ] AC-11: Required Review, compliance, reference-rights, and work-fact conflicts block formal progress as defined; compliance has no user or administrator bypass.
- [ ] AC-12: Actual external release confirmation binds exact content, packaging, chapter range, platform, time, and evidence and atomically creates the sole active Cycle for the task.
- [ ] AC-13: Material external differences use the abnormal observation/Cycle path and can never be rewritten into a normal valid Cycle.
- [ ] AC-14: Feedback distinguishes numeric, true zero, unavailable, not applicable, and not entered; corrections preserve history and invalidate dependent analysis.
- [ ] AC-15: AI analysis remains a candidate until confirmed; “continue observing” creates no formal `HumanDecision`, keeps the Cycle active, records a new observation point/reason, and returns to feedback; only a separately confirmed human decision normally closes a valid Cycle.
- [ ] AC-16: For the adjacent valid pair Cycle N/N+1, the current formal Cycle N decision produces an actual scoped change used by the Cycle N+1 external release; invalid Cycle numbers are not reused, and the product continues to later Cycle numbers instead of ending automatically after the first valid pair.
- [ ] AC-17: Two consecutive valid real Cycles pass every PRD 7.6 checklist item without a severe trust incident.

## AI Execution, Cost, and Policy — Must Pass

- [ ] AC-18: Execution preview shows target/input version, active Agent roles, actual models/providers, data/reference scope, candidate count, required Review, estimated time/cost, remaining budget, and provider-policy state.
- [ ] AC-19: Actual Agent/model participation and handoffs satisfy AC-19A, AC-19B, and AC-19C cumulatively; five required novel roles and the three approved provider families complete the PRD validation evidence by V1.2.
- [ ] AC-20: Agent execution topology is read-only; there is no free Agent creation, Prompt editing, arbitrary wiring, custom DAG persistence, or general Workflow Builder.
- [ ] AC-20A: Production A05 is an administrator-only immutable Prompt registry/evaluation/promotion surface, not a raw Prompt editor. It shows `PromptConfigBundle`, `EvaluationBinding`, and safe `ExecutionBinding` identities, applicable release/workload, evaluation evidence, lifecycle, champion/optional last-known-good, actor separation, activation history, and audit without secrets, protected inputs, or hidden holdout content.
- [ ] AC-20B: Automated checks cannot advance a Prompt beyond `OfflinePassed`. Human approval and production activation are distinct authorized actions; missing/stale/failed evidence or insufficient author/reviewer/activator separation fails closed, while revoke and rollback preserve immutable history and authoritative receipts. A first version uses `ExplicitPilot` and, on stop, disables the affected AI capability plus routes to a deterministic/manual flow; it never invents a last-known-good target.
- [ ] AC-21: One user-level paid slot covers model-dependent Bot and business execution; queues, cancellation-before-start, partial completion, retry, model switching, and incurred costs remain explicit.
- [ ] AC-22: Budget warning at 80% and blocking at 100% work without silently skipping mandatory steps or switching models.
- [ ] AC-23: Provider green/yellow/red policy and current model/config versions are evaluated for each execution; screenshots are excluded from model input.

## UIUX, Recovery, and Accessibility — Must Pass

- [ ] AC-24: Every page state has exactly one visually primary action and exposes disabled reasons and recovery paths.
- [ ] AC-24A: Release capability is consistent across navigation and entry surfaces. A later-release route/action cannot leak through a direct link, Bot/action card, pending/activity item, export, or administrator surface; missing/unknown/stale capability never defaults to enabled. This proposed child assertion is effective only after the roadmap UIUX overlay is approved.
- [ ] AC-25: Long-form manuscript, formal status, evidence, and next action retain priority over AI graphics, cards, metrics, or process detail.
- [ ] AC-26: Independent loading, empty, failure, stale, offline, saving, save-failed, blocked, partial, queued, cancelled, and recovery states preserve valid data and user input and satisfy AC-26A through AC-26C cumulatively. A visible stale/last-known-good result is never presented as current, and recovery never bypasses a formal gate.
- [ ] AC-27: At `1440+` and `1280–1439`, desktop layouts keep formal state and the primary action usable and overlay secondary context before reducing manuscript usability. At `768–1279`, compact workspace normally preserves authorized desktop capabilities and reflows navigation, evidence, comparison, tables, drawers, and dialogs without hiding critical fields, status, disabled reasons, or the one primary action. If a specific formal action cannot safely show its complete preview, that action alone fails closed with an explicit 1280 × 720 requirement and cannot submit a reduced payload.
- [ ] AC-28: At `0–767`, including 390 × 844, approved content and read-only decision evidence are readable while Bot input/action application, complex creation/editing, human-review completion, execution, formal confirmation, release, decision, every D10 mode including resume, and admin are disabled with an explanation. D11 preview/download of an already generated approved package and D12 simple survey are the only package-defined exceptions.
- [ ] AC-29: Core flows support keyboard operation, visible focus, focus restoration, semantic landmarks, associated errors, reduced motion, and state communication by text + icon + color.
- [ ] AC-30: Visual implementation uses the approved semantic tokens and contrast requirements and does not introduce neon dashboards, dense KPI walls, or AI decoration across manuscript content.

## Governance, Export, Deletion, and Operations — Must Pass

- [ ] AC-31: Reference provenance, rights, selected fragments, actual use, deletion impact, and Prompt-injection treatment are traceable.
- [ ] AC-32: Export packages cumulatively satisfy AC-32A through AC-32C, bind exact versions/evidence, and preserve required AI/reference declarations.
- [ ] AC-33: Lifecycle, restore/recovery, and retention behavior cumulatively satisfies AC-33A through AC-33C and matches PRD state transitions and confirmed deployment targets.
- [ ] AC-34: Administrator configuration cumulatively satisfies AC-34A through AC-34C, affects only eligible new execution, preserves historical associations, and records debug content access with reason/scope/audit.
- [ ] AC-35: No product claim promises automated publishing, platform approval, exposure, growth, signing, income, causality, or market validation.

## Deterministic Critical Scenarios

| Scenario | Required result |
|---|---|
| Bot failure/policy block | Continue work, pending, task list, and structured Stage 0 remain usable; original input/context is preserved |
| Ambiguous Bot request | User chooses the target task/object/action; the system never guesses from recency |
| Candidate confirmation | Primary candidate remains non-formal until Review, confirmation, and memory gates complete |
| Decision candidate | Evidence is inspectable, but an invalid/unknown/stale reference, abstention, required human review, deterministic-validation block, or compliance-policy block cannot fall through to an executable action; the UI never attributes an authoritative block to the model candidate, and human review still precedes normal formal confirmation |
| V1.0 task enters V1.1 | The user completes `OperationValidationBaseline`; the prior `CreationBaseline`, executions, snapshots, and audit history remain unchanged, and no operation field is silently backfilled |
| Actual release | One command binds immutable release facts and creates exactly one active Cycle or creates neither |
| Feedback correction | Old snapshot remains, dependent formal analysis becomes stale, and a new confirmation path is required |
| Continue observing | A new observation point and reason are recorded, no formal human-decision record is created, the Cycle remains active, and the primary path returns to feedback |
| Partial model failure | Successful outputs and costs remain; only failed parts receive a new attempt; mandatory missing Review blocks confirmation |
| Offline/stale save | Text and context remain; formal actions are disabled until compare/sync/review succeeds |
| System degradation | The affected scope shows `degradationMode`, named capabilities, freshness/`asOf`, retry eligibility/timing, preserved work, and one safe recovery action. Drafts, formal writes, reads, AI candidates, and objects follow their distinct safety rules; 429/503 never cause an unbounded or unsafe replay |
| Prompt promotion | Automated evaluation stops at `OfflinePassed`; independent approval, activation, and revoke are distinct audited actions. A first version exercises ExplicitPilot plus AI-disable/manual fallback; a later version can exercise last-known-good rollback only when that target is verified |
| Release capability | A later-release route is absent from normal navigation; direct access shows current-release unavailability and a safe return without exposing the action |
| Compact workspace | At 768–1279, authorized business capability normally survives reflow with formal state, evidence, disabled reasons, and the single primary action intact; an unsafe formal preview fails closed explicitly rather than losing fields |
| Mobile | Formal content and read-only evidence are readable; all D10 modes including resume explain that desktop is required |

## Automatic Failure

- AI/Agent/administrator output is presented as user-confirmed fact.
- A formal record is overwritten, a retry hides an old attempt/cost, or release/Cycle state becomes inconsistent.
- Bot text or a drawer directly confirms business state, starts business execution without preview, or performs task control.
- The UI exposes a general Workflow Builder, arbitrary Agent wiring, free Prompt tuning, or a market/template platform.
- A production Prompt is raw-edited in A05, auto-approved/activated, activated without current evaluation and human evidence, or rolled back by overwriting history.
- A first Prompt version is shown with a fabricated last-known-good target, or a stop condition leaves its affected AI capability enabled instead of routing to the deterministic/manual flow.
- A `SemanticFindingCandidate`, model-self-reported confidence, judge result, any future calibrated hint, or recommended action becomes an authoritative next action, formal fact, human decision, or mutation permission, or a deterministic/compliance block is presented as a model-returned decision.
- A missing, unauthorized, wrong-version, invalid, or stale evidence reference is silently discarded while the rest of the candidate remains adoptable.
- A normal Cycle exists without confirmed real external release evidence, or closes normally without a valid human decision.
- “Continue observing” is stored as a formal human decision, closes the Cycle, or satisfies a single-Cycle/two-Cycle completion gate.
- Mobile enables any D10 mode or other prohibited business operation, compact workspace loses an authorized critical action/evidence field, or 1280 desktop hides the formal state/primary action.
- After overlay approval, a future-release route/action leaks through an entry surface without the required release capability.
- A page has peer primary actions, inaccessible status, fake progress, silent data loss, or an unexplained disabled control.
- A stale or last-known-good view omits `asOf`, cached data is labeled current, a local-only draft says `已保存`, a 429/503 causes unbounded retry, or a formal command/paid AI/object-finalize operation is blindly replayed.

## Required Evidence

- Maintain a release trace row for every applicable requirement with: authoritative source and requirement/subassertion ID, first-due release, cumulative status, module/data owner, implementation/test evidence, and release gate. Child assertions record Passed, Failed, N/A, or Unverified; a split parent with any future/incomplete child records `Partially qualified / Unverified`, never Passed.
- Map every due PRD 7.5 row and PRD 7.6 item to its first release and cumulative evidence. V1.2 must contain the complete PRD 7.5/7.6 matrix; V1.0/V1.1 must not mark not-yet-due rows Passed or N/A merely because they are scheduled later.
- Map UIUX state-matrix scenarios 1-130 to a first-due release and implementation tests; representative screenshots never replace behavioral assertions. A versioned UIUX delta must be approved before any scenario is treated as deferred from its original full-V1 package state.
- Preserve the package inventory fact: 55 scenarios are `exact` and 75 are `representative`; representative and generic template references do not prove a page-specific visual result. Every one of the 130 scenarios still requires a behavioral assertion.
- Capture the package-designated 1440 × 900, 1280 × 720, and 390 × 844 baselines. Existing package coverage has only two 1280 and two 390 screenshots, so it cannot prove all pages, dialogs, A05, decision-candidate, compact-workspace, or phased-release states.
- For each release critical path, add exact page-specific visual evidence for default, blocked/stale/degraded, candidate/formal, and completion states at applicable wide/desktop/compact/mobile viewports. At minimum, V1.0 covers creation, decision-candidate review, and AC-26A recovery; V1.1 covers P04/P05, the one-valid-Cycle outcome, and AC-26B; V1.2 covers comparable/partially comparable/not-comparable, value result, the following Cycle N+2 entry (Cycle 3 on the normal 1→2 path), and AC-26C; A05 covers evaluation, approval, ExplicitPilot/Shadow, activation, revoke, first-version no-LKG fallback, and later-version rollback. Missing approved designs remain Unverified.
- Verify `768–1279` at a recorded representative width and verify boundaries at 767/768 and 1279/1280; compact workspace must not invoke mobile read-only.
- Decision-candidate behavior tests cover valid evidence, counterevidence, contradiction, missing/unauthorized/wrong-version locator, unknown enum, invalid schema, abstain, required human review, stale input, human accept/edit/reject/request-evidence, and no mutation before normal confirmation.
- AC-26A/26B/26C evidence follows the H0/H1/H2 first-due table in [System Degradation and Recovery UIUX](SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md). It covers every common field, the five operation classes, 429/503 with and without `Retry-After`, save/conflict/result-unknown, one CTA, mobile read-only, focus/announcement, and page-specific exact designs at due viewports. All such evidence remains `Unverified` until approved and executed.
- A05 tests cover the three Binding identities, lifecycle transitions, automated stop at `OfflinePassed`, actor separation, missing/stale evidence, judge-human disagreement, ExplicitPilot/Shadow authority, activation conflict/idempotency, emergency revoke, first-version no-LKG AI-disable/manual fallback, later-version last-known-good rollback, queued/running execution impact, compact reflow, keyboard/focus, and audit receipt.
- V2.0 requires a separately approved financial scenario matrix and visual set; novel scenarios 1-130, P03/P05 screenshots, or Prompt results cannot serve as financial completion evidence.
- Run only repository-defined checks from `../engineering/TECH_STACK.md`; unavailable tooling remains Unverified.
- Real Cycle acceptance requires real external release/feedback evidence. Simulated data supports functional rehearsal only.
- Apply all due Confirmed reliability and performance gates; targets do not prove results.
