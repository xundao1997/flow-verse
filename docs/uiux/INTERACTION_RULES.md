# FlowVerse Interaction Rules

## Status and Authority

- Retained interaction behavior from the external package identified by `../intake/V1_PACKAGE_INTAKE.md` remains the approved baseline.
- The cumulative-release, DecisionCandidate, Prompt-governance, compact-workspace, mobile-D10 conflict-resolution, and system-degradation/recovery additions are `IN_REVIEW / Proposed`. They cannot authorize implementation or acceptance until the synchronized change set receives explicit final human approval.

## Primary Flow

    login and session recovery
      → work home: Bot or deterministic entry
      → Stage 0 baseline
      → candidates and Review
      → formal content and memory confirmation
      → release plan and manual external release
      → atomic actual-release confirmation + Cycle creation
      → feedback snapshot
      → formal analysis
      → human decision
      → next actual change and Cycle N

## Page Contract

Every page or auxiliary surface makes these clear:

1. Which task, Cycle, object, version, and authority context is active?
2. Is the visible item a candidate, formal fact, observation, analysis, suggestion, or human decision?
3. What single action should happen next, what will it change, and why might it be disabled?
4. What was preserved when loading, saving, execution, network, policy, or validation failed?
5. If the page is degraded, which capabilities are affected, how fresh is the visible data, when may recovery be attempted, and is a verified fallback actually available?

## Release Capability and Route Contract

- The complete approved V1 journey remains the superset design contract. If this overlay is approved, a release may expose only the page, subpage, dialog, action, and state set explicitly assigned in `RELEASE_CAPABILITY_MATRIX.md`; implementation does not infer a split from scenario number or route availability.
- Under this `IN_REVIEW` overlay, navigation, deep links, work-home cards, pending items, Bot action cards, activities, export entries, and administrator navigation must consume one server-authoritative release-capability result after approval. The proposed matrix is its UI presentation contract; a client-side feature flag is not an independent source of business permission.
- A route or action not introduced in the current release is absent from ordinary navigation. Direct or stale deep links render an explicit unavailable state with current release, requested capability, preserved return target, and the nearest safe available route; they never fall through to a nearby action or generic permission error.
- A capability present in the release but blocked by task state remains visible with its business blocking reasons. A capability absent from the release must not be misrepresented as a task-state failure or as a disabled control that promises an unapproved delivery date.
- Unknown, missing, expired, or stale release capability fails closed for writes and AI execution. Read-only history may remain visible only when the server authorizes that exact resource.
- If the overlay is approved, V1.0 completion must not deep-link into release/feedback/decision work; V1.1 can end after its one-valid-Cycle outcome without exposing V1.2 comparison/value/following-Cycle controls; V1.2 owns the next-round, adjacent-valid-Cycle N/N+1 effect, and following Cycle N+2 surfaces. V2.0 requires its own financial product, UIUX, and acceptance contract and cannot reuse novel routes or scenarios as completion evidence.

## Work Home and Bot

- Bot, continue work, pending summary, and task list load and fail independently.
- The embedded Bot and global Bot drawer share conversation, context, composer, action cards, and unapplied drafts.
- A Bot message may explain, navigate, or organize only user-provided information into a previewable draft. It cannot create novel content, Review, analysis, release facts, metrics, comments, or formal state.
- Business AI actions navigate to the owning page and open the approved execution preview. Formal or dangerous actions only navigate to their owning page.
- Action cards carry target context, input revision, expiry, scope, cost/wait, missing data, and blockers; they revalidate before execution.
- Task switching saves drafts, closes auxiliary surfaces, clears writable old-task context/subscriptions, and prevents old conversation content from entering the new task.

## Candidate and Formal Commands

- Setting a primary candidate, editing a candidate, accepting an important risk, confirming formal content, and confirming memory are distinct actions.
- Human edits create a new candidate with provenance; MVP does not perform paragraph-level intelligent merge.
- Formal commands use an idempotency key and expected revision, show a current preview, prevent duplicate submission, and wait for a server receipt.
- On uncertain network outcome, query command status before allowing another attempt.
- On version conflict, preserve input, show the change source and difference path, then require refresh/review.
- Formal records, attempts, corrections, and replacements are never optimistically overwritten.

## Decision Candidate Review

- A semantic decision run returns a read-only `SemanticFindingCandidate` to the page that owns the related business object. It cannot update capability, next action, form values, formal facts, or task/Cycle state.
- `DecisionCandidatePanel` presents the candidate question and version, model-originated status (`candidate`, `abstain`, or `needs_human_review`), recommendation label, evidence references, contradictions, missing evidence, risks, alternatives, and human-review reasons. Model-self-reported confidence is omitted by default; only a separately approved, human-calibrated coarse hint may be introduced later. The panel never displays hidden reasoning or invents a citation when no locator exists.
- Evidence references open the exact authorized source/version/locator and identify `supports`, `challenges`, or `context`. Deleted, unauthorized, unresolvable, wrong-version, or stale references cause the deterministic validator to mark the whole candidate invalid/non-adoptable; visually plausible partial text is not retained as a valid recommendation.
- `abstain` and `needs_human_review` are normal safe model states, not failures to hide. They show what is missing, how to add/correct evidence, and where authorized desktop human review occurs. A deterministic validation block or authoritative compliance-policy block is displayed separately with its owner/reason and has no adoption action; it never appears among the semantic candidate statuses.
- If the deterministic layer already supplies one legal next action, the panel is secondary evidence and cannot replace that primary action. If multiple legal low-risk actions remain, the page uses one primary “审阅并选择下一步” action; option selection is not itself a formal mutation.
- Human review records keep reviewer, decision, reason, evidence version, candidate version, and time. A review outcome can accept, edit into a new human-authored draft, reject, or request more evidence, but the normal formal confirmation and submit-time capability revalidation still apply.

## AI Execution and Agent Trace

- Every paid business execution passes through a preview showing target, input version, active roles, model/provider, data scope, references, candidate count, required Review, time/cost estimate, budget, and provider-policy state.
- `CreationBaseline` owns the initial-batch model/language/budget/rights boundaries and candidate-count initial value. Advanced Settings only versions future defaults inside those boundaries; expanding a boundary routes to baseline replacement and impact review. D01 shows and `ExecutionBinding` freezes the actual values, and per-reference rights/use evidence remains required.
- One user-level paid slot is shared by model-dependent Bot calls and business execution; deterministic entry points never depend on it.
- Retry or model switching creates a new attempt. Partial completion preserves successful outputs and incurred cost and permits recovery only for failed parts.
- The trace is read-only. User checkpoints deep-link to the owning object rather than exposing a generic “approve” button in the graph.

## Prompt Registry, Evaluation, and Promotion

- A05 lists immutable Prompt families/versions, complete `PromptConfigBundle` and eligible `EvaluationBinding` identities/hashes, safe `ExecutionBinding` audit references, applicable product release/workload, evaluation status, current champion, optional last-known-good, activation scope, and audit links. Production administrators do not edit raw Prompt text or arbitrary rules in this surface.
- Evaluation details separate deterministic hard gates, representative/incident/hidden-set evidence, objective scores, blind pairwise results, human findings, judge-human disagreement, cost, latency, robustness, and drift. Hidden holdout content, secrets, and unrestricted model output remain unavailable.
- The visible lifecycle is `Draft → Candidate → OfflinePassed → HumanApproved → ExplicitPilot/Shadow → ControlledCanary → Active → Deprecated/Revoked/RolledBack`. Each transition exposes only the actions allowed from the current state; automated evaluation cannot cross `OfflinePassed`.
- The proposed Prompt-governance contract treats human approval, production activation, emergency revoke, and rollback as distinct explicit actions with author/evaluator/activator duty separation, change reason, expected revision, idempotency protection, impact preview, and authoritative receipt. Exact role-to-permission mapping requires auth approval; a single actor cannot approve their own change end to end.
- ExplicitPilot/Shadow/challenger results are labeled with their actual authority: shadow/challenger cannot create user candidates, influence the page's next action, perform tools, or write formal state; ExplicitPilot is limited to the approved allowlist and guards. Their cost/data scope must already have been disclosed through the applicable execution flow.
- Missing, stale, failed, or unlicensed evaluation evidence disables promotion and activation. Evaluation service failure may preserve a Draft/Candidate and any prior Active version, but it cannot select a locally cached or merely newest version. Emergency revoke and last-known-good rollback stay separately auditable.
- For the first Prompt version, A05 explicitly shows `无可回退的已验证版本`. The controlled path is `HumanApproved → ExplicitPilot → ControlledCanary → Active`; a stop condition disables the affected AI capability and exposes the deterministic/manual recovery flow. `回退至已验证版本` is unavailable until a later verified last-known-good exists.

## Cycle and External Facts

- Initial creation is outside every Cycle.
- Confirming an actual external release and creating its Cycle are one atomic action.
- External material differences create an abnormal observation/Cycle path; history cannot later be rewritten as a normal valid Cycle.
- Feedback distinguishes numeric value, true zero, unavailable, not applicable, and not entered.
- “Continue observing” adds an observation point and keeps the Cycle active.
- Only a confirmed human decision can normally close a valid Cycle; AI analysis and recommendations never do so.

## Error, Offline, and Recovery

- The common user-visible authority is [System Degradation and Recovery UIUX](SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md). Every affected page/section uses the same `degradationMode`, `affectedCapabilities`, `dataFreshness`/`asOf`, `retryable`/`retryAfter`, and optional verified `lastKnownGoodRef` semantics; unknown or contradictory values fail closed for writes and AI.
- Ordinary drafts save after the approved debounce, flush on risky navigation, and remain locally pending offline.
- Offline mode disables AI execution and every formal mutation but preserves drafts, context, scroll, and selected object.
- Save failure or stale input disables dependent formal actions while preserving user text. A local-only recovery copy says `已保存在此设备，尚未同步`; only an authoritative server receipt/revision may say `已保存到服务器`.
- Long tasks show accepted/queued/failed promptly and a real stage/update or external-wait explanation at the approved interval.
- Cancellation only claims what the underlying lifecycle supports; in-flight work and incurred cost remain visible.
- A stale or validator-invalidated semantic candidate remains inspectable where authorized but cannot be adopted; refresh uses a new candidate/version rather than silently replacing the old evidence.
- If release capability cannot be loaded, preserve page data and return navigation but disable every capability-dependent write and AI action.
- If Prompt activation or evaluation evidence is unavailable, existing formal content remains readable while new Prompt promotion and affected AI preview/start actions fail closed with an owner-facing recovery path.

## Common Degradation, Freshness, and Retry

- Ordinary draft save may fail open only to an explicitly local unsynced draft. Formal writes, dangerous commands, paid AI/model switching, object finalize/manifest inclusion, and any unknown result fail closed; read-only data may remain only as an authorized stale or verified last-known-good view with `asOf`.
- A formal command with an uncertain outcome exposes `查看处理结果` as the sole primary recovery action and queries the existing receipt. It never offers a peer primary submit or blindly replays the command.
- A 429 or 503 does not itself authorize retry. The UI honors server-provided `retryable` and `retryAfter`; only an approved idempotent read may retry automatically within approved finite attempt/time/visibility budgets. Until those budgets exist, retry is manual. Navigation, logout, task/account switch, or a superseding request cancels the one retry owner/timer.
- Provider/Prompt failure disables only affected AI capability and preserves deterministic/manual work; ObjectStore failure disables only affected upload/verification/processing/download/export capability and never turns metadata into proof that bytes exist. PostgreSQL/authority uncertainty closes formal writes and current-authority reads.
- A degraded page still has one visually primary CTA. If the ordinary primary action remains safe, status/retry is secondary; if exactly one authoritative recovery is safe, it replaces the blocked primary action. If none is safe, the primary action returns to a safe available route.
- Mobile degradation cannot widen the `0–767px` capability set. D11 can retry only an already generated authorized package whose object is currently available; D12 simple-survey input may be preserved locally, but submission still requires current capability and a receipt.
- H0/V1.0 first proves AC-26A; H1/V1.1 regresses it and proves AC-26B on P04/P05; H2/V1.2 regresses both and proves AC-26C on next-round/comparison/value. All new exact and behavioral evidence remains `Unverified`.

## Responsive Capability

- `1440+` uses wide desktop composition; `1280–1439` keeps desktop composition with secondary context in an overlay where specified.
- `768–1279` is compact workspace, not mobile read-only. It normally preserves authorized desktop capabilities and the one primary action while converting multi-column layouts, evidence sidebars, comparison panels, wide tables, drawers, and dialogs into labeled single-column sections or one exclusive full-height overlay. No critical field or disabled reason may exist only in a collapsed/hidden column. When a specific formal preview/confirmation cannot safely show its complete required fields in the actual viewport/input environment, only that action fails closed and explains that at least the approved 1280 × 720 desktop environment is required; it cannot submit a reduced payload or switch the whole workspace silently to mobile semantics.
- `0–767` is mobile read-only for business work. It allows navigation, task/status/formal-content reading, authorized Bot history, read-only Agent timeline, and read-only decision evidence. It disables Bot input/action application, candidate adoption/comparison, human review completion, AI execution, formal mutation, release, decision, all D10 task controls including resume, and all administrator actions.
- The only approved-package mobile write exception is the D12 simple survey. D11 permits preview/download of an already generated approved package but no range reconfiguration or generation. Neither exception authorizes another modal or business mutation.
- Responsive state does not rely on User-Agent as authorization. The official renderer fails closed and uses a short-lived presentation reference only to prevent stale route/layout submission; the server independently applies role, ownership, revision, policy and formal business guards. Neither a client-supplied mode nor that reference proves physical viewport or blocks a non-official client that claims desktop mode. Universal device enforcement requires a separately approved managed-client/attestation contract and is not claimed here.

## Overlays and Accessibility

- Bot, Agent collaboration, pending, and advanced settings drawers are mutually exclusive; activity is a popover, not a fifth drawer.
- Dialogs trap focus, support appropriate Escape behavior, make the background inert, and restore focus.
- Disabled controls remain focusable when needed to explain reasons.
- Status uses text, icon, and color. Unknown progress uses phase text rather than a fake progress bar.
- Degradation status names the affected scope, freshness and full `asOf` time, preserved work, and recovery. Routine changes use a polite live region; a newly blocking failure may alert once, but unchanged polling and countdown ticks are not repeatedly announced.
- At mobile read-only width, unavailable actions remain explained instead of silently disappearing.
- Decision evidence uses semantic lists/tables with claim-to-source relationships in text, preserves focus when a locator opens/closes, and announces `abstain`, blocking, stale, and human-review-required states without relying on color.
- A05 version/evaluation comparisons retain headers and hidden-column detail at compact width; promotion, revoke, and rollback dialogs name the exact version, scope, impact, and verified last-known-good target before the action. If none exists, rollback is absent/disabled and the dialog names the AI-capability-disable plus deterministic/manual recovery instead.
