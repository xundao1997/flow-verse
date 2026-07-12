# FlowVerse V1 Performance Budget

## Policy

- Performance targets and success thresholds require user or approved-package confirmation.
- Apply performance work only to affected scenarios; otherwise record N/A with reason.
- AI must not relax, delete, or reinterpret a confirmed budget to make a change pass.
- Read package scope from ../intake/V1_PACKAGE_INTAKE.md and technology facts from TECH_STACK.md.
- This file owns latency, throughput, bundle, interaction, and memory measurement.
- RELIABILITY_BUDGET.md owns availability/error, deadline/retry, idempotency, concurrency/backpressure, recovery, and failure-control targets; reference its row IDs instead of duplicating limits.

## Proposed Web Field SLO Reference

These values are reference proposals, not release gates, until the approved V1 scope confirms a Web product and the user accepts them:

| Metric | Proposed target | Measurement | Gate stage | Status |
|---|---|---|---|---|
| Largest Contentful Paint (LCP) | ≤ 2.5 s | Field p75, mobile and desktop separate | Post-release | Proposed |
| Interaction to Next Paint (INP) | ≤ 200 ms | Field p75, mobile and desktop separate | Post-release | Proposed |
| Cumulative Layout Shift (CLS) | ≤ 0.1 | Field p75, mobile and desktop separate | Post-release | Proposed |

- Official reference: [Web Vitals](https://web.dev/articles/vitals).
- A browser main-thread task longer than 50 ms is a Long Task to investigate, not a zero-count release rule. See [Optimize long tasks](https://web.dev/articles/optimize-long-tasks).
- Pre-release lab results never prove field p75.

## Gate Model

- Intake: confirm applicability, owner, critical scenarios, measurement plan, environment, data scale, and target source.
- Bootstrap: create only approved measurement entry points, verify commands, establish noise, and record the first production-build baseline.
- Implementation / pre-release: applicable Confirmed Lab budgets for the current slice must pass.
- Post-release: collect Confirmed Field metrics for the approved page scope, sample rule, and window.
- Before sufficient field data exists, status is PendingFieldData. This is not “Passed” and does not block the first release unless the user explicitly makes it a pre-release gate.

## Budget Registry

| Budget area | Applicability | Gate stage | Type | Target / warning / failure | Environment or scale | Evidence | Status | Owner |
|---|---|---|---|---|---|---|---|---|
| Target browsers and devices | Unknown | Intake | Lab / Field | TBD — do not infer | TBD | None | Unknown | User |
| Lab CPU, network, and cache | Unknown | Bootstrap | Lab | TBD — do not infer | TBD | None | Unknown | User |
| RUM tool and page scope | Unknown | Post-release | Field | TBD — do not infer | TBD | None | Unknown | User |
| Field sample and time window | Unknown | Post-release | Field | TBD — do not infer | TBD | None | Unknown | User |
| JS / CSS / font / image / transfer | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Homepage and route readiness | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Chapter length and history scale | Unknown | Intake | Test data | TBD — do not infer | TBD | None | Unknown | User |
| Rendered DOM / window bound | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| History, chat, and cache capacity | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Typing, Chinese IME, selection, scroll | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Background persistence, if approved | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| API latency and throughput measurement | Unknown | Pre-release | Lab / Field | TBD — do not infer | TBD | None | Unknown | User |
| AI visible response and completion | Unknown | Pre-release | Lab / Field | TBD — do not infer | TBD | None | Unknown | User |
| AI streaming buffer, if approved | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| AI context size, token, and cost measurement | Unknown | Implementation | Lab / Field | TBD — do not infer | TBD | None | Unknown | User |
| Throughput and saturation measurement | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Memory and long-session growth | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Regression warning / failure delta | Unknown | Post-bootstrap | Lab / Field | TBD after noise baseline | TBD | None | Unknown | User |

Applicability values: Required, Optional, Unknown, N/A.

Status values: Proposed, Confirmed, Conflict, Unknown, N/A, PendingFieldData.

When a budget's Gate stage becomes due for the active slice, Applicability must first become Required, Optional, or N/A; Applicability Unknown blocks classification. A Required budget must then be Confirmed and pass. Optional, unrelated, or later-stage entries do not block but cannot support a pass claim while Unknown.

## Critical Scenarios

- Web homepage cold start and return visit, when Web delivery is confirmed
- Open an existing creation and switch approved routes or panels
- Long-document typing, Chinese IME, selection, scrolling, undo, and redo
- Continue typing safely during approved save or background-persistence behavior, when such behavior exists
- Start, cancel, retry, and recover an AI request; test stream buffering only when streaming is approved
- Long editing session with confirmed bounds for DOM, memory, history, chat, world data, cache, and AI context

Optimization must not break drafts, consistency, accessibility, IME, cursor, selection, undo history, or error recovery.

## Measurement Workflow

1. Determine whether the change affects a registered scenario; if not, record N/A with reason.
2. Use the Confirmed production build, tool, command, device, network, cache, and test data.
3. Declare affected loading, interaction, rendering, network, memory, AI, and bundle metrics.
4. Establish a before baseline under identical conditions.
5. For local experiments, run at least five repetitions and compare median plus raw results; do not label this field p75/p95.
6. Repeat measurement and functional safety checks after the smallest implementation change.
7. Record raw data, delta, bundle changes, Long Tasks, memory, and limitations.
8. If warning/failure deltas are not yet Confirmed, report every repeatable difference and request risk acceptance; do not claim “no regression”.
9. Fix, revert, or request explicit risk acceptance when a Confirmed applicable budget fails.
10. Without a baseline or Confirmed tool, report Unverified; never claim “optimized”.

## Hard Engineering Constraints

- Confirm and enforce performance/resource bounds for applicable lists, history, chat, world data, DOM, cache, and AI context.
- Use operational deadline, retry, concurrency, backpressure, and recovery limits only from Confirmed RELIABILITY_BUDGET.md rows.
- Requests, streams, polling, timers, and workers that can outlive or be superseded by a user action require cancellation and cleanup.
- When an underlying operation cannot be cancelled, document why and provide timeout, stale-response protection, and lifecycle cleanup.
- If AI streaming is approved, batch rendering; do not rerender an entire conversation or manuscript per token.
- Cache design states key, lifetime, capacity, invalidation, ownership, and consistency risk.
- New dependencies require measured bundle, runtime, startup, memory, maintenance, and security impact.
- Do not introduce Worker, Service Worker, CDN, global/persistent cache semantics, backend protocol, global memoization, or blanket lazy loading without evidence and approval.
- Local reversible optimizations may proceed within an approved task when measurement supports them.
- Backend work must avoid N+1 access and unbounded reads; indexes require query evidence.
- Multi-agent execution is not the default for simple tasks; measure latency, context, tool calls, tokens, and cost under Confirmed reliability fan-out/concurrency/retry limits.

## Performance Handoff

For affected scenarios, report build, environment, data scale, tool and command, baseline, budget, raw results, after-result, delta, stage, pass/fail/unverified status, functional safety, and remaining risk. Otherwise report N/A with reason.
