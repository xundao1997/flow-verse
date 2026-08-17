# FlowVerse System Degradation and Recovery UIUX Contract

## Status and Authority

**Status: `IN_REVIEW / Proposed`.**

- This document defines the common user-visible presentation and interaction contract for degraded, stale, retryable, and recovery states across V1.0, V1.1, and V1.2. It does not approve an API Schema, implementation, dependency, retry threshold, deployment topology, or reliability result.
- The external UIUX package identified by [V1 Package Intake](../intake/V1_PACKAGE_INTAKE.md) remains unchanged. This contract is a repository overlay and requires explicit overall human approval before implementation or acceptance.
- The server remains authoritative for capability, permission, revision, freshness, retry eligibility, receipt, and recovery. The client never infers safety from HTTP reachability, cached data, elapsed time, viewport, or a locally remembered success.
- Exact and behavioral designs, fixtures, implementation, E2E, accessibility, performance, failover, and recovery evidence are all `Unverified`.

## 1. Common Degradation View Contract

Every affected page or independently failing section consumes one server-authoritative degradation result. The minimum shared semantic fields are:

| Field | Proposed UI meaning | Mandatory presentation rule |
|---|---|---|
| `degradationMode` | Closed mode describing the safe presentation posture, including normal, partial, read-only, stale-read, offline-draft, retry-later, or capability-disabled behavior | Unknown, missing, or contradictory values fail closed for writes and AI. The exact transport enum is frozen with the approved interface contract, not invented by the renderer |
| `affectedCapabilities` | Stable capability references affected by the condition | Disable or constrain only the named capabilities. Do not turn a local provider/object failure into an unexplained whole-product outage, and do not enable an unlisted action by omission |
| `dataFreshness` | Closed freshness class: current, stale, verified last-known-good, or unknown | Stale, last-known-good, and unknown are visibly distinct from current. Unknown freshness cannot authorize a formal action |
| `asOf` | Authoritative timestamp for the visible snapshot | Required for `stale` and `verified last-known-good`; display in the user's locale with an accessible full timestamp. For `unknown`, it may be null only when no authoritative timestamp exists, in which case the UI says the freshness time is unknown. Never manufacture it from browser cache time |
| `retryable` | Whether the exact failed operation is currently safe to retry | A true value permits only the recovery operation named by the authoritative contract; it never makes a formal command or paid AI call generally repeatable |
| `retryAfter` | Server-directed earliest retry time or delay, including an HTTP `Retry-After` result for applicable 429/503 responses | Show a calm time-based instruction and prevent premature automatic retry. Absence means the UI does not invent a countdown or retry schedule |
| `lastKnownGoodRef` | Optional verified reference to an authorized prior snapshot/configuration/result | Show the referenced version and `asOf`; never substitute a cache blob or merely newest item. If absent, say that no verified fallback exists |

The transport may carry an error ID, reason code, preserved-input status, and allowed recovery actions in addition to these fields. Copy is mapped from approved stable codes; raw stack traces, provider bodies, object locators, secrets, or infrastructure names never reach the user.

### 1.1 Scope and precedence

- A section-level failure remains in that section when independent navigation, saved text, or other sections are safe. A page-level banner is used only when the condition changes the whole page's interpretation or primary action.
- The most specific authoritative result wins: actor/object/action capability over page capability, and current server evidence over cached UI state. A broad status cannot re-enable a more-specific block.
- Every degraded state says: what is affected, what remains available, whether visible data is current, what input/result was preserved, and the single safest next action.
- Recovery never bypasses role, ownership, release capability, mobile capability, expected revision, idempotency, policy, compliance, or formal-confirmation gates.

## 2. Operation-Class Safety Matrix

| Operation class | Default failure posture | What may remain available | Required recovery behavior |
|---|---|---|---|
| Ordinary draft save | **Fail open only to an explicitly local, unsynced draft** when the approved local repository is available | Current user input, selection/context, prior server-saved revision, local export where approved | Say `已保存在此设备，尚未同步` rather than `已保存`; dependent formal actions remain disabled. Reconnect compares the server revision before sync and routes conflicts to review |
| Formal write or dangerous command | **Fail closed**; never optimistically complete or silently resubmit | Read-only preview, entered data, idempotency/receipt lookup, safe navigation | If the outcome is unknown, the sole primary recovery is to query the command receipt/status. A new submit is offered only after the authoritative result proves it safe and the full preview is revalidated |
| Read-only query | **May fail open to an authorized stale or verified last-known-good snapshot** only when the server contract allows that resource to be shown | Labeled historical content, navigation, local draft, unaffected independent sections | Always show `dataFreshness` and `asOf`. Any action requiring current authority remains disabled until a current refresh succeeds |
| AI candidate or model-dependent Bot action | **Fail closed for new model calls, adoption, and formal progress** when provider, Prompt evidence, policy, budget, or binding is unavailable/unknown | Deterministic entry, manual workflow, saved/formal content, prior authorized candidate as visibly non-authoritative history | Preserve partial outputs and incurred cost. Never automatically rerun, switch model, select newest Prompt, or treat an old candidate as current. Recovery returns to a new preview or the deterministic/manual path |
| Object upload, verification, processing, download, or export | **Fail closed for the affected object capability** when existence, integrity, authorization, or storage availability cannot be proven | PostgreSQL-backed task navigation, text/formal metadata, local ordinary draft, unaffected objects | Never report upload/download/export success from metadata alone. Resume only the approved idempotent transfer step with the same authorized session/version; finalize, manifest inclusion, and formal reference require fresh authoritative verification |

Authentication or authoritative PostgreSQL uncertainty always closes formal writes and any read requiring current authority. Static shell and an approved local ordinary draft may remain available, but cached content is never relabeled as current.

## 3. 429/503 and Bounded Retry

- `429` and `503` are not generic invitations to loop. The UI uses `retryable` and `retryAfter` from the same authoritative response; status code alone does not decide retry safety.
- Automatic retry is eligible only for an approved idempotent read and only within the approved attempt, elapsed-time, and visibility budgets. Until those budgets are frozen, the safe default is manual retry. Exact counts and delays are intentionally not selected here.
- A valid `Retry-After` is honored. One resource has one retry owner and one timer; navigation, logout, task/account switch, a superseding request, or page disposal cancels it. Multiple sections do not create a retry storm.
- Formal writes, dangerous commands, paid AI calls, model switching, object finalize, and unknown provider outcomes are never automatically replayed. Formal result uncertainty queries the existing receipt; AI recovery creates a new reviewed attempt; object recovery resumes only an approved idempotent stage.
- If `retryable=false`, no retry control is shown as an active promise. The UI gives the safe alternative: preserve draft, view stale authorized data, return to deterministic/manual work, inspect status, or contact the named support/owner path when one is approved.
- A countdown is informational, not a fake progress indicator. It does not announce every second to assistive technology; announce the initial restriction and when retry becomes available.

## 4. Saving, Conflict, and Result-Unknown States

| Visible state | User-facing meaning | Formal-action rule |
|---|---|---|
| Editing / unsaved | Input exists only in the current editing buffer | Disabled when the action requires a saved revision |
| Saving | One bounded save is in flight; later input is still preserved separately | Never imply success; do not submit a formal command against an unknown revision |
| Saved to server | An authoritative save receipt/revision was received | Formal action may proceed only after all other current gates pass |
| Saved on this device, not synced | Local recovery copy exists; server revision is not current | Formal action disabled; sync/compare is the single recovery path |
| Save failed | Input is preserved, but neither server save nor local fallback may be assumed beyond what is explicitly confirmed | Offer the one safe retry/export/recovery action and retain focus/context |
| Conflict / stale base | Server and local revisions differ | Show source/version difference and require compare/review; never last-write-wins silently |
| Formal result unknown | Request left the client, but no authoritative receipt is known | Primary action is `查看处理结果`; no duplicate formal submission |

On viewport transition into mobile read-only, unsubmitted desktop input is preserved as an eligible local draft or visibly unsaved buffer. The transition never submits, discards, or converts it into a formal record.

## 5. One Primary CTA During Degradation

- The page continues to have exactly one visually primary action. A degradation banner does not add a peer primary retry button when the normal safe primary action remains valid.
- If the normal primary action is blocked and one recovery step is both safe and authoritative, that recovery step becomes the sole primary action. Examples are `重新加载最新状态`, `比较并同步草稿`, or `查看处理结果`.
- If no immediate recovery is safe, keep the blocked reason visible and use a safe navigation action as primary. Passive status, copy-to-support ID, details, dismiss, and manual refresh are secondary.
- A section retry remains secondary unless that section is the page's only legal next step. Repeated 429/503 responses cannot create multiple competing retry CTAs.
- Disabled controls are not the only explanation. The reason and recovery path remain keyboard reachable and associated with the affected action.

## 6. Responsive and Mobile Recovery

- Wide desktop, 1280 desktop, and compact workspace preserve the same degradation meaning, freshness, preserved-work statement, and primary action. Reflow cannot hide `asOf`, the affected capability, or the recovery reason.
- At `0–767px`, mobile remains read-only for prohibited business work even when retry becomes available. Recovery cannot enable Bot input/action application, candidate adoption/comparison, human-review completion, AI execution, formal mutation, release, decision, D10, administrator actions, or D11 generation.
- D11 may retry preview/download only for an already generated authorized package and only when object availability is currently proven. Metadata or `lastKnownGoodRef` alone does not prove downloadable bytes.
- D12 simple survey remains the sole package-defined mobile write exception. During degradation, input may be visibly preserved locally, but formal submission still requires current server capability and an authoritative receipt.
- The mobile explanation remains `请使用桌面端继续此操作` for width-prohibited actions; a system outage or stale-data reason is shown separately so the user is not told that changing devices will repair a service failure.

## 7. Accessible Status and Recovery

- The degradation summary is a named status region linked to the affected heading/action. It uses text, icon, and color and exposes the full timestamp and affected scope to assistive technology.
- Routine loading/retry updates use a polite live region. A newly blocking failure may use an alert once; repeated polling, countdown ticks, and unchanged status are not repeatedly announced.
- Focus stays on the initiating control or preserved input after an inline failure. If recovery opens a dialog or comparison, standard focus trap, Escape policy, inert background, and focus restoration apply.
- A status update never clears typed text, collapses the active evidence location, moves focus without request, or replaces a detailed error with color alone.
- Keyboard users can reach the reason, freshness details, recovery action, and support/error ID. Reduced-motion settings apply to reconnect/status transitions, and unknown duration uses phase text rather than animated fake progress.

## 8. H0/H1/H2 First-Due Contract

| Gate | AC child assertion | First-due degradation coverage | Evidence status |
|---|---|---|---|
| H0 / V1.0 | `AC-26A` | Shared shell, P01, Stage 0, P02, P03, A05 and V1.0 D11; all five operation classes; 429/503; local draft/save/conflict/result-unknown; mobile read-only; provider/Prompt/ObjectStore partial failure | Exact design and behavior evidence `Unverified` |
| H1 / V1.1 | `AC-26B` | H0 regression plus P04/P05, packaging/release, external facts, feedback draft/snapshot, analysis candidate/formal analysis, human decision, D04-D09/D12 reconciliation; stale external evidence cannot authorize release or decision | Exact design and behavior evidence `Unverified` |
| H2 / V1.2 | `AC-26C` | H0/H1 regression plus decision-driven next round, comparison/value, following Cycle N+2, complete export, and D12 simple survey; stale prior-Cycle facts cannot appear current or drive a new formal action | Exact design and behavior evidence `Unverified` |

A later gate cannot retroactively qualify an earlier one. Every newly introduced surface reruns the common field, operation-class, one-CTA, mobile, accessibility, and retry assertions.

## 9. Required Review Evidence

- Behavior fixtures cover each common field as present, absent, stale, contradictory, unknown, and changed during a request; unknown values close affected writes/AI without losing input.
- Each operation class covers current success, partial dependency failure, offline, 429 with/without `Retry-After`, retryable and non-retryable 503, superseding navigation, repeated failure, and recovery.
- Formal-command tests cover before-send failure, result unknown, receipt lookup, same-key/same-intent recovery, conflict, and prevention of duplicate submission. AI tests preserve attempt/cost and never auto-rerun. Object tests never infer bytes or integrity from metadata.
- Visual review covers default and blocking degradation at 1440 × 900, 1280 × 720, one approved compact width, and 390 × 844, plus behavior at 767/768 and 1279/1280. Page-specific exact evidence is required where the degradation changes the primary action or hides an otherwise available capability.
- Accessibility evidence includes keyboard order, visible focus, status naming, focus retention/restoration, polite versus alert announcement, countdown behavior, zoom/text spacing, contrast, reduced motion, and screen-reader reading of scope/freshness/`asOf`/recovery.
- No evidence exists merely because this document is complete. Until approved designs, implementation, fixtures, commands, raw results, and owner review exist, every new exact and behavioral assertion remains `Unverified`.
