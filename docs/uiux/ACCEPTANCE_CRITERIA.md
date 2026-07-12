# FlowVerse V1 Acceptance Criteria

## Release Identity

- [ ] AC-00: V1 is implemented as the first release without inferred v0.x behavior, migration, compatibility, or redesign requirements.

## Must Pass

- [ ] AC-01: The first screen makes it clear that creation can begin by talking to AI.
- [ ] AC-02: The homepage is not a marketing page, Dashboard, module chooser, or traditional SaaS workbench.
- [ ] AC-03: The AI assistant is the primary navigation entry.
- [ ] AC-04: Users do not need to choose or understand a space before expressing intent.
- [ ] AC-05: A complex task generates a creative workspace while a simple task stays in conversation.
- [ ] AC-06: The chapter page gives the manuscript editor the dominant area and visual priority.
- [ ] AC-07: Story health uses risk, reason, suggestion, and blocking status; it does not use scores or KPIs.
- [ ] AC-08: World state is expressed as creative insight, not charts or an analytics Dashboard.
- [ ] AC-09: No UI suggests a draggable Workflow Builder or exposes Agent / Prompt configuration.
- [ ] AC-10: Every page state has one visually primary CTA and a clear next step.
- [ ] AC-11: Colors are low-saturation and comfortable for long reading; body text is never pure black.
- [ ] AC-12: The UI is usable at 1440 × 900 and 390 × 844 CSS pixels with keyboard and visible focus.
- [ ] AC-13: The first screen shows the FlowVerse 流界 brand Logo; zh-CN navigation uses the fixed labels in COPY_RULES.md.

## Deterministic Scenarios

| Scenario | Example input | Expected result |
|---|---|---|
| Simple conversation | “帮我润色这句话。” | Stay in conversation; do not create or ask the user to choose a workspace. |
| Complex creation | “帮我从零构建一个长篇小说世界，并开始创作第一章。” | Generate a creative workspace without a manual space chooser. |
| Blocking health risk | A fixture marked blocking | Show “回到正文修改” as primary; forward confirmation is hidden or disabled. |
| Non-blocking health risk | A fixture marked non-blocking | Show “进入世界历史确认” as primary; revision may be secondary. |

## Observable Layout Checks

- At both verification viewports, the Logo, greeting, and primary AI input are visible without scrolling.
- At 1440 × 900, the manuscript is the largest continuous chapter-workspace pane.
- At 390 × 844, manuscript content is primary and auxiliary regions do not cause horizontal scrolling.
- Required text and controls meet the contrast thresholds in DESIGN_TOKENS.md.

## Automatic Failure

- The product resembles Dify, an enterprise admin console, or a BI Dashboard.
- AI appears only as a peripheral chat plug-in.
- Users must distinguish world, knowledge, and creation spaces before starting.
- Cards or status panels crowd out the chapter editor.
- Black-purple neon, scan lines, uncontrolled particles, or high-saturation blue dominate.
- A health check reduces story quality to a score.
- A page presents multiple peer primary actions.

## Required Evidence

- Record each criterion as pass, fail, or not applicable with a reason.
- Capture visual evidence at both verification viewports for homepage, chapter editor, world insight, and both health-check states.
- Run repository-defined lint, build, typecheck, tests, and accessibility checks when available.
- Never mark an unavailable check as passed; record the missing tooling and residual risk.

## Performance Must Pass

- [ ] PERF-01: Every applicable Confirmed Lab budget due for the active pre-release gate in ../engineering/PERFORMANCE_BUDGET.md passes in its defined environment.
- [ ] PERF-02: Each due budget classifies Applicability as Required, Optional, or N/A; Applicability Unknown blocks the active slice, and every Required budget is Confirmed and passes before that gate completes.
- [ ] PERF-03: Long-document typing, Chinese IME, selection, scrolling, and undo/redo preserve correctness under the approved scale.
- [ ] PERF-04: When background persistence or AI streaming is approved, its correctness and performance scenarios pass; applicable DOM, memory, cache, history, and context performance bounds have Confirmed values and verification.
- [ ] PERF-05: Performance-sensitive changes record same-environment before/after data; unaffected changes record N/A with reason and never substitute a diagnostic score for field or approved Lab criteria.
- [ ] PERF-06: Confirmed Web Field SLOs are evaluated post-release when sufficient approved field data exists; PendingFieldData is not Passed and does not block the first release unless the user explicitly requires it.
