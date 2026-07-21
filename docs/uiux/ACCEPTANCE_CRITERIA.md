# FlowVerse V1 Acceptance Criteria

## Authority and Release Identity

- These repository IDs summarize the approved PRD v1.1 sections 7.5-7.10 and UIUX `DesignSpec/state_matrix.json` scenarios 1-130.
- The PRD matrix and Cycle validity checklist remain authoritative when this summary is less specific.
- V1 is the first implemented release; earlier direction-document provenance creates no migration or compatibility acceptance.

## Product and Trust — Must Pass

- [ ] AC-01: The default user and administrator complete first-login password change, lockout, session expiry, and hard role isolation; administrators cannot impersonate users or confirm user business facts.
- [ ] AC-02: P01 presents the shared Bot, continue work, pending summary, and complete task list as independent regions; model/Bot failure does not block deterministic entry.
- [ ] AC-03: Bot context always identifies global/task/Cycle/object scope; ambiguity requires an explicit mutually exclusive choice and task switching does not leak writable context.
- [ ] AC-04: Bot text alone changes no task, draft, Cycle, formal object, or execution. Action cards revalidate target/revision/policy/budget before any permitted action.
- [ ] AC-05: Business AI requests route to the owning page and execution preview; formal and dangerous actions route to their owning page and cannot be confirmed from the work home or drawer.
- [ ] AC-06: Stage 0 confirms and freezes the creative start, platform, scope, indicators, observation points, model/budget choices, language, and validation goal.
- [ ] AC-07: One novel task isolates its content, references, executions, versions, releases, feedback, and Cycles from every other task.
- [ ] AC-08: Candidate, primary candidate, human-edited candidate, accepted risk, formal content, work memory, observation, analysis, recommendation, and human decision remain visibly and behaviorally distinct.
- [ ] AC-09: AI output never becomes formal implicitly; all formal content, memory, packaging, release, feedback, analysis, and decision records require the default user's explicit confirmation.
- [ ] AC-10: Every formal content confirmation creates an immutable complete snapshot; retry, model switching, correction, and replacement preserve prior records and costs.
- [ ] AC-11: Required Review, compliance, reference-rights, and work-fact conflicts block formal progress as defined; compliance has no user or administrator bypass.
- [ ] AC-12: Actual external release confirmation binds exact content, packaging, chapter range, platform, time, and evidence and atomically creates the sole active Cycle for the task.
- [ ] AC-13: Material external differences use the abnormal observation/Cycle path and can never be rewritten into a normal valid Cycle.
- [ ] AC-14: Feedback distinguishes numeric, true zero, unavailable, not applicable, and not entered; corrections preserve history and invalidate dependent analysis.
- [ ] AC-15: AI analysis remains a candidate until confirmed; “continue observing” keeps the Cycle active; only a confirmed human decision normally closes a valid Cycle.
- [ ] AC-16: Cycle 1 decision produces an actual change used by the next external release; the product continues to Cycle N and does not end automatically after Cycle 2.
- [ ] AC-17: Two consecutive valid real Cycles pass every PRD 7.6 checklist item without a severe trust incident.

## AI Execution, Cost, and Policy — Must Pass

- [ ] AC-18: Execution preview shows target/input version, active Agent roles, actual models/providers, data/reference scope, candidate count, required Review, estimated time/cost, remaining budget, and provider-policy state.
- [ ] AC-19: Actual Agent/model participation and handoffs are traceable; five required novel roles and the three approved provider families participate as required by PRD validation evidence.
- [ ] AC-20: Agent execution topology is read-only; there is no free Agent creation, Prompt editing, arbitrary wiring, custom DAG persistence, or general Workflow Builder.
- [ ] AC-21: One user-level paid slot covers model-dependent Bot and business execution; queues, cancellation-before-start, partial completion, retry, model switching, and incurred costs remain explicit.
- [ ] AC-22: Budget warning at 80% and blocking at 100% work without silently skipping mandatory steps or switching models.
- [ ] AC-23: Provider green/yellow/red policy and current model/config versions are evaluated for each execution; screenshots are excluded from model input.

## UIUX, Recovery, and Accessibility — Must Pass

- [ ] AC-24: Every page state has exactly one visually primary action and exposes disabled reasons and recovery paths.
- [ ] AC-25: Long-form manuscript, formal status, evidence, and next action retain priority over AI graphics, cards, metrics, or process detail.
- [ ] AC-26: Independent loading, empty, failure, stale, offline, saving, save-failed, blocked, partial, queued, cancelled, and recovery states preserve valid data and user input.
- [ ] AC-27: 1440 × 900 and 1280 × 720 desktop layouts keep formal state and the primary action usable; compact desktop overlays secondary context before shrinking the manuscript.
- [ ] AC-28: At 390 × 844, approved content is readable while Bot input, complex creation/editing, execution, formal confirmation, release, decision, task control, and admin are disabled with an explanation.
- [ ] AC-29: Core flows support keyboard operation, visible focus, focus restoration, semantic landmarks, associated errors, reduced motion, and state communication by text + icon + color.
- [ ] AC-30: Visual implementation uses the approved semantic tokens and contrast requirements and does not introduce neon dashboards, dense KPI walls, or AI decoration across manuscript content.

## Governance, Export, Deletion, and Operations — Must Pass

- [ ] AC-31: Reference provenance, rights, selected fragments, actual use, deletion impact, and Prompt-injection treatment are traceable.
- [ ] AC-32: Export packages bind exact versions and preserve required AI/reference declarations.
- [ ] AC-33: Pause, terminate, archive, delete, restore/recovery, and retention behavior match PRD state transitions and confirmed deployment targets.
- [ ] AC-34: Administrator configuration is versioned, affects only eligible new execution, preserves historical associations, and records debug content access with reason/scope/audit.
- [ ] AC-35: No product claim promises automated publishing, platform approval, exposure, growth, signing, income, causality, or market validation.

## Deterministic Critical Scenarios

| Scenario | Required result |
|---|---|
| Bot failure/policy block | Continue work, pending, task list, and structured Stage 0 remain usable; original input/context is preserved |
| Ambiguous Bot request | User chooses the target task/object/action; the system never guesses from recency |
| Candidate confirmation | Primary candidate remains non-formal until Review, confirmation, and memory gates complete |
| Actual release | One command binds immutable release facts and creates exactly one active Cycle or creates neither |
| Feedback correction | Old snapshot remains, dependent formal analysis becomes stale, and a new confirmation path is required |
| Partial model failure | Successful outputs and costs remain; only failed parts receive a new attempt; mandatory missing Review blocks confirmation |
| Offline/stale save | Text and context remain; formal actions are disabled until compare/sync/review succeeds |
| Mobile | Formal content is readable; prohibited actions explain that desktop is required |

## Automatic Failure

- AI/Agent/administrator output is presented as user-confirmed fact.
- A formal record is overwritten, a retry hides an old attempt/cost, or release/Cycle state becomes inconsistent.
- Bot text or a drawer directly confirms business state, starts business execution without preview, or performs task control.
- The UI exposes a general Workflow Builder, arbitrary Agent wiring, free Prompt tuning, or a market/template platform.
- A normal Cycle exists without confirmed real external release evidence, or closes normally without a valid human decision.
- Mobile enables high-risk business operations, or 1280 desktop hides the formal state/primary action.
- A page has peer primary actions, inaccessible status, fake progress, silent data loss, or an unexplained disabled control.

## Required Evidence

- Record every applicable AC ID plus every PRD 7.5 matrix row and PRD 7.6 Cycle checklist item as Passed, Failed, N/A, or Unverified with exact evidence.
- Map UIUX state-matrix scenarios 1-130 to implementation tests; representative screenshots never replace behavioral assertions.
- Capture visual evidence at 1440 × 900, 1280 × 720, and 390 × 844 for the package-designated states.
- Run only repository-defined checks from `../engineering/TECH_STACK.md`; unavailable tooling remains Unverified.
- Real Cycle acceptance requires real external release/feedback evidence. Simulated data supports functional rehearsal only.
- Apply all due Confirmed reliability and performance gates; targets do not prove results.
