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
| Target browsers and devices | Required | Intake | Lab / Field | Chrome and Edge latest two major versions; desktop primary; mobile business surfaces read-only | 1440 × 900 baseline; 1280 × 720 minimum desktop; 390 × 844 mobile evidence | PRD v1.1 section 7.9 and UIUX tokens/package | Confirmed | User/product |
| Lab CPU, network, and cache | Unknown | Bootstrap | Lab | TBD — do not infer | TBD | None | Unknown | User |
| RUM tool and page scope | Unknown | Post-release | Field | TBD — do not infer | TBD | None | Unknown | User |
| Field sample and time window | Unknown | Post-release | Field | TBD — do not infer | TBD | None | Unknown | User |
| JS / CSS / font / image / transfer | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Homepage and route readiness | Required | Pre-release | Lab | Ordinary open/switch/filter/save feedback P95 <= 2s, excluding model and file-processing wait; deterministic work-home regions meet this during Bot failure | Approved browsers/viewports; exact dataset and command TBD | PRD v1.1 section 7.9 | Confirmed target; measurement plan Unknown | User/product |
| Chapter length and history scale | Required | Intake | Test data | Initial validation default: 20-chapter outline plus first 3 chapters; long-session/history upper bounds still require confirmation | One real novel task; exact characters/bytes/versions TBD | PRD v1.1 sections 3.8 and 7.1 | Proposed pending engineering scale | User |
| Rendered DOM / window bound | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| History, chat, and cache capacity | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Typing, Chinese IME, selection, scroll | Unknown | Pre-release | Lab | TBD — do not infer | TBD | None | Unknown | User |
| Background persistence, if approved | Required | Pre-release | Lab | Save status visible <= 2s after user action; draft save starts after 5s idle; formal confirmation saves immediately | Approved editor dataset and interruption scenarios TBD | PRD v1.1 section 7.9 | Confirmed target; measurement plan Unknown | User/product |
| API latency and throughput measurement | Required | Pre-release | Lab / Field | Ordinary page actions P95 <= 2s; exact boundary breakdown and throughput target TBD | One default user + one admin MVP; approved lab command TBD | PRD v1.1 section 7.9 | Confirmed latency target; remaining plan Unknown | User/product |
| AI visible response and completion | Required | Pre-release | Lab / Field | Status <= 2s after Bot send/business start; understandable update or explicit external wait at least every 10s; execution deadline 30m; reference usable-state target 3m | Approved provider scenarios and raw timing command TBD | PRD v1.1 section 7.9 | Confirmed target; measurement plan Unknown | User/product |
| AI streaming buffer, if approved | Unknown | Implementation | Lab | TBD — do not infer | TBD | None | Unknown | User |
| AI context size, token, and cost measurement | Unknown | Implementation | Lab / Field | TBD — do not infer | TBD | None | Unknown | User |
| Throughput and saturation measurement | Required | Implementation | Lab | One user paid slot; one business step per task; up to three model calls within a step; queues remain responsive and cancellable before start | One user + admin MVP; exact backlog/queue capacity TBD | PRD v1.1 sections 3.10 and 7.9; reliability registry | Confirmed concurrency bound; capacity plan Unknown | User/product |
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

## Diagnostic-bootstrap baseline

- Scope: the non-business Check page adds one user-triggered Web → API → Worker diagnostic path. It does not add product data, AI execution, caching, streaming, timers or background polling.
- Production build, Windows, Node.js 24.17.0, pnpm 11.10.0, Vite 8.1.4, `corepack pnpm@11.10.0 --dir services/web run build`, final execution on 2026-07-21: HTML 0.63 kB / 0.43 kB gzip; CSS 4.76 kB / 1.65 kB gzip; JavaScript 195.52 kB / 62.22 kB gzip; build transform reported 129 ms. This is a one-execution raw baseline, not a product release budget or field-performance claim.
- A superseded request is cancelled and stale responses cannot overwrite current state. The page checks once on load and only again after the single explicit action; polling and retry are absent.
- The API → Worker deadline is two seconds with zero retries. A PostgreSQL-connected functional chain returned 200 locally on 2026-07-30; controlled end-to-end latency remains Unverified because no repeatable timing scenario has been approved or measured.
- Application container image sizes/startup, CI build duration/cache behavior, application remote-deployment duration and field Web Vitals remain N/A until those targets and measurement environments are separately approved. Server-middleware image size/startup/steady-state measurements are now applicable but Unverified because the current host has no Docker runtime.
- Product AI latency, throughput, editor interaction, memory and long-session budgets are N/A for this non-business diagnostic slice.

## Server-middleware capacity baseline

The `FV1-LOCAL-MIDDLEWARE-DIAGNOSTIC` command adds three concurrent bounded control-plane probes only. It changes no product interaction, bundle or workload throughput budget; no latency claim is made from a single developer-network run.

- Scopes `FV1-SERVER-MIDDLEWARE-DEPLOY` and `FV1-SERVER-DATA-EXTENSIONS` are operational capacity plans, not measured throughput or latency SLOs. They change no product interaction budget.
- The lightweight middleware-only test plan is at least 4 vCPU, 8 GiB RAM and 1 TiB SSD/NVMe. Use at least 8 vCPU and 16 GiB RAM before co-locating application services or running concurrent ingestion, indexing, backup or compaction. Configured service limits are PostgreSQL 2 CPU/2 GiB, Redis 1 CPU/1 GiB and MinIO 1 CPU/1 GiB.
- TimescaleDB preload remains inside the PostgreSQL limit, with two Timescale background workers inside six PostgreSQL worker processes. PostgreSQL uses 512 MiB shared buffers and 50 connections; Redis `maxmemory` is 512 MiB below its 1 GiB container limit. These are bounded lightweight defaults, not evidence that future stock/RAG load fits the allocation; BuildKit source compilation also needs separate transient host headroom.
- Persistent-volume capacity targets are PostgreSQL 300 GiB, Redis 20 GiB and MinIO 500 GiB, with at least 15% host free space. Compose labels document these values; host partitions/LVM and alerts must enforce them.
- The corrected images built and all three containers reached `healthy` in one target-server smoke, but no controlled build duration, startup duration, steady-state memory, disk I/O, RAG ingestion, vector-query, object-transfer or Redis load result was measured. All performance/capacity results remain Unverified until representative data, load and a repeatable measurement command are available.
