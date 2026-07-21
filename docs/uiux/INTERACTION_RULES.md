# FlowVerse Interaction Rules

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

## AI Execution and Agent Trace

- Every paid business execution passes through a preview showing target, input version, active roles, model/provider, data scope, references, candidate count, required Review, time/cost estimate, budget, and provider-policy state.
- One user-level paid slot is shared by model-dependent Bot calls and business execution; deterministic entry points never depend on it.
- Retry or model switching creates a new attempt. Partial completion preserves successful outputs and incurred cost and permits recovery only for failed parts.
- The trace is read-only. User checkpoints deep-link to the owning object rather than exposing a generic “approve” button in the graph.

## Cycle and External Facts

- Initial creation is outside every Cycle.
- Confirming an actual external release and creating its Cycle are one atomic action.
- External material differences create an abnormal observation/Cycle path; history cannot later be rewritten as a normal valid Cycle.
- Feedback distinguishes numeric value, true zero, unavailable, not applicable, and not entered.
- “Continue observing” adds an observation point and keeps the Cycle active.
- Only a confirmed human decision can normally close a valid Cycle; AI analysis and recommendations never do so.

## Error, Offline, and Recovery

- Ordinary drafts save after the approved debounce, flush on risky navigation, and remain locally pending offline.
- Offline mode disables AI execution and every formal mutation but preserves drafts, context, scroll, and selected object.
- Save failure or stale input disables dependent formal actions while preserving user text.
- Long tasks show accepted/queued/failed promptly and a real stage/update or external-wait explanation at the approved interval.
- Cancellation only claims what the underlying lifecycle supports; in-flight work and incurred cost remain visible.

## Overlays and Accessibility

- Bot, Agent collaboration, pending, and advanced settings drawers are mutually exclusive; activity is a popover, not a fifth drawer.
- Dialogs trap focus, support appropriate Escape behavior, make the background inert, and restore focus.
- Disabled controls remain focusable when needed to explain reasons.
- Status uses text, icon, and color. Unknown progress uses phase text rather than a fake progress bar.
- At mobile read-only width, unavailable actions remain explained instead of silently disappearing.
