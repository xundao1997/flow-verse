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
| Original target browsers and package viewports | Required | Intake | Lab / Field | Chrome and Edge latest two major versions; desktop primary; package mobile business surfaces are read-only subject to the recorded D10 conflict | 1440 × 900 baseline; 1280 × 720 minimum full desktop; 390 × 844 mobile evidence | PRD v1.1 section 7.9 and UIUX tokens/package | Confirmed | User/product |
| Compact-workspace and responsive conflict overlay | Unknown | Intake | Lab / Field | `768–1279` normally preserves authorized desktop capability; `0–767` disables all D10 modes, with only the named D11/D12 package exceptions | One approved representative compact width plus 767/768 and 1279/1280 behavior | `../uiux/RELEASE_CAPABILITY_MATRIX.md` (`IN_REVIEW`) | Proposed | User/product/design |
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
| System-decision Prompt and JIT call-start overhead | Unknown | Pre-release for each AI-enabled version | Lab / Field | Measure deterministic precheck, context assembly, atomic call-start lock/revalidation/commit, provider latency, post-validation, candidate-to-page readiness, token/cost, and explicit human-review time separately. BUSINESS and EVALUATION use separate pool/cost series；EVALUATION分DIRECT/PAIRED、PROMPT_ONLY/FACTORIAL/BASELINE_GATE basis、CANDIDATE/CONTROL arm、TARGET/JUDGE role与OFFLINE/SHADOW authorization，并单列依赖等待、resolved-call-input构建、typed baseline artifact/authority读取、run artifact聚合到API finalizer的等待/失败/Unverified时间；BASELINE_GATE不得计入虚构control provider latency/cost，DIRECT不得被统计为独立promotion gate；exact thresholds TBD | Each active PromptConfig × model × family × representative input tier, plus approved evaluation binding/basis/arm/role profile. Bounded `promptFamily/modelProfile/provider/workloadClass/evaluationArm/evaluationCallRole` labels are allowed；comparison basis/authorization kind只能低基数；Prompt body/config/version/ref, judge config/version, hashes, callIntent and per-execution IDs are forbidden metric labels | `V1_TECHNICAL_SOLUTION_PROPOSAL.md` sections 9.5–9.12; `../ai/SYSTEM_DECISION_PROMPTS.md`; Proposed ADR-0029 | Proposed; measurement Unverified | AI governance / product |
| Throughput and saturation measurement | Required | Implementation | Lab | One user paid slot; one business step per task; up to three model calls within a step; queues remain responsive and cancellable before start | One user + admin MVP; exact backlog/queue capacity TBD | PRD v1.1 sections 3.10 and 7.9; reliability registry | Confirmed concurrency bound; capacity plan Unknown | User/product |
| N-1 fault-domain capacity | Unknown | Only when `UD-AVL-01` makes AvailabilityGate applicable | Lab / Failure exercise | After loss of one approved fault domain, remaining Web/API/Worker/PG/ObjectStore capacity must still meet the approved latency/queue budgets or enter the approved explicit degradation mode; replica counts and headroom TBD. This row never blocks baseline H0 when AvailabilityGate is not applicable and never replaces DataSafety recovery evidence | Approved production topology and representative peak/burst/backlog workload | `V1_TECHNICAL_SOLUTION_PROPOSAL.md` sections 12.5–13.8; RELIABILITY_BUDGET FV1-ROADMAP-REVIEW rows | Proposed | Delivery/operations |
| H0 fixed-input benchmark profile | Unknown | H0 pre-release | Lab / Failure exercise | Fixed inputs: <=20 files/task, <=10 MB/file, <=500,000 characters/file, <=2,000,000 characters/task, <=300 pages/text PDF; representative default 20-chapter outline + first 3 chapters is adjustable and not a hard ceiling. Run short/target/limit × cold/warm; environment, resources, network, concurrency/queue, samples/noise, commands and per-test warning/failure thresholds require approval | H0 physical allowlist only; Web/API/PG/ObjectStore/Worker paths plus recovery/degradation where due | PRD v1.1; `../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md`; Proposed ADR-0023 | Proposed; measurement Unverified | User/product/performance owners TBD |
| Per-release physical contract census | Unknown | H0/H1/H2 contract gate | Static / Lab | Future business release manifest must expand exact approved columns/constraints, public/internal method/paths and internal jobType/family/schema/capability overlay. Current Proposed grouping covers 103 logical tables as H0 76 + H1 delta 22 + H2 delta 5, 107 Public catalog rows as H0 79 + H1 delta 23 + H2 delta 5, and 10 business Internal rows physically due at H0 with version-scoped overlays; no gap/overlap and no V2 item. Count/digest is a scope guard, not a throughput result. A separate operational manifest retains exactly five rows: API `OPS-API-001..003` (`GET /health/live`, `GET /health/ready`, `GET /health/dependencies`) and private Worker `OPS-WORKER-001..002` (`GET /health/live`, `GET /health/ready`); none count toward the 107/10 business catalogs or release-capability claims | `T001–T103`, `PUB-001–PUB-107` and `INT-001–INT-010` mapping in `V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`; only current cumulative business gate may exist physically. Production H0 denies the Web Check page, public `GET /api/v1/system/chain`, and `GET /internal/v1/system/status` together and proves no API→Worker diagnostic dependency, while preserving only the separately allowlisted five `OPS-*` health routes | Proposed ADR-0011/0013/0021; data/interface design section 10.2 | Proposed; verification Unverified | Architecture/data/API owners TBD |
| Worker claim fairness, pool isolation and retire recovery | Unknown | Before first async business workload | Lab / Failure exercise | Measure empty-claim rate/backoff, queue age/service time by bounded workload class/pool, high-priority saturation with low-priority sentinel wait, claim lock/pool wait, lease loss, heartbeat/grant response-unknown recovery, stop-claim drain, WAITING_DIAGNOSIS/RETIRED volume, DeliveryStore fill/oldest, grant-intent orphan backlog, unreceipted-index lag/backlog/HWM scan duration/gap failures, DELIVERY_RECOVERY/DELETION_DISPOSITION/no-payload disposition age/success/failure and result-ack latency. Failure fixtures assert typed ownership: AI state stays on execution, document state on P03 reference processing, and export state on D11 export request; new document processing and export generation fail closed. Exact weights, intervals, pool sizes, limits and thresholds TBD | H0 workload mix plus API outage, Worker retirement, provider outcome unknown, GET-input无副作用、POST-grant提交后响应丢失、同reportKey异hash拒绝、payload-before-record/index crash、grant-intent存在但index无entry、index-before-ack crash、分页gap/duplicate、producer buffer后首次report前丢失、pre-barrier call结果晚到→仅隔离处置buffer、删除barrier后普通迟到buffer拒绝、no-payload finalizer与late payload并发、逐locator不存在/secure-erase proof及DeliveryStore capacity fault；任何边界不可证时cleanup不得COMPLETE。verify PostgreSQL-backed formal content stays readable and only an already generated authorized package with current ObjectStore proof remains previewable/downloadable; no per-job high-cardinality labels | `V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`; Proposed ADR-0013/0018 | Proposed; measurement Unverified | Execution/operations/performance owners TBD |
| ObjectStore business/DataSafety and optional Availability capacity | Unknown | H0 object slice; N-1 only when AvailabilityGate applies | Lab / Failure exercise | After live-auth conformance, H0 measures streaming upload/head/range/read, finalize/hash, concurrent transfer, quarantine/commit, lifecycle/delete, backup/restore and consistent-cut behavior without API whole-file buffering. Cross-fault-domain and N-1 are added only for an applicable AvailabilityGate. Health or admin ListBuckets is not a business result; exact throughput/concurrency/capacity thresholds TBD | Fixed H0 file tiers plus approved object count/version/retention profile; fault-domain profile only when applicable | `V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`; Proposed ADR-0015/0018/0022 | Proposed; measurement Unverified | Object/platform/performance owners TBD |
| Cross-store checkpoint/manifest scale | Unknown | DataSafetyGate / production pre-release | Lab / Recovery exercise | Compare the approved consistent-cut algorithm at representative object/reference/deletion scale: cut transaction duration, shard build/checksum/Merkle time, strict component-manifest generation/signature time, metadata growth, ledger lag/replay, restore validation and RTO contribution. Component manifest必须固定PG cut、对象分片/Merkle、ledger HWM、schema/config、compatible application artifact和runbook ref/hash/version。No unbounded MVCC transaction, list or metric label; exact shard/page/frequency thresholds TBD | Approved recovery set and H0/H1/H2 cumulative physical allowlist; cold restore, interrupted/repeated reconciliation and component missing/hash mismatch cases | Proposed ADR-0018; RELIABILITY_BUDGET cross-store row | Proposed; measurement Unverified | Data/operations/performance owners TBD |
| Redis/Timescale activation trigger measurement | Unknown | Before any first business use | Lab | Current baseline is direct PG + PG durable jobs and ordinary PG records. Only sustained measured query/lock/queue/retention/aggregation breach plus quantified benefit may trigger one specific Redis role or Timescale extension; baseline, shadow comparison, migration/backfill and rollback must be recorded | Same workload/data/environment before and after; Redis role labels bounded; V1 novel must show zero Timescale schema and zero Redis authoritative dependency | `V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`; Proposed ADR-0023 | Proposed; activation Unverified | Data/platform/performance owners TBD |
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
