# FlowVerse UIUX Principles

## Authority and Direction

The approved direction is an **editorial workbench with restrained AI presence**: warm, calm, traceable, recovery-oriented, and suitable for long-form writing. Exact contracts and visual references come from the UIUX package identified in `../intake/V1_PACKAGE_INTAKE.md`.

## Product Hierarchy

1. Current formal content, evidence, and business state.
2. The single next action allowed by the current state.
3. Candidate differences, Review findings, and user decisions.
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

## Agent and Workflow Visualization

- Show only actually activated business roles and actual model participation.
- Agent execution is a read-only trace with inputs, handoffs, versions, attempts, partial results, cost, failures, and user checkpoints.
- Do not expose free Agent creation, Prompt editing, arbitrary wiring, topology mutation, custom DAG persistence, or a general Workflow Builder.
- Agent detail supports understanding and recovery; it is not an independent chat surface or first-level product area.

## Primary Action and States

- Exactly one action receives primary visual emphasis in each page state.
- Disabled formal actions remain discoverable and explain every blocking reason and recovery path.
- Loading, empty, failure, stale, offline, partial, budget, policy, compliance, unsaved, and cancellation states preserve valid content and deterministic navigation.
- Progress shows real stage, updated time, completed outputs, and cost; never fabricate a percentage.

## Reading, Responsive, and Accessibility

- Baseline: 1440 × 900. Minimum desktop: 1280 × 720.
- At wide desktop, keep the writing surface dominant and contextual regions secondary.
- At compact desktop, convert fixed context into an overlay before reducing manuscript usability.
- At 390 × 844, preserve readable task/status/formal content; disable complex creation, Bot execution, formal confirmation, release, decision, task control, and admin with “请使用桌面端继续此操作”.
- Maintain keyboard navigation, visible focus, semantic landmarks, focus return, error association, reduced motion, and non-color state cues.

## Avoid

- Sci-fi dashboards, neon graphs, animated data-flow spectacle, dense KPI walls, or decoration competing with text.
- Treating AI output, Agent summaries, or administrator actions as user-confirmed fact.
- Hiding formal state or the primary action at 1280 desktop width.
- Multiple peer primary actions, invisible disabled reasons, destructive ambiguity, or silent optimistic formal updates.
