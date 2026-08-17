# FlowVerse UIUX Release Capability Matrix — IN_REVIEW

## Authority and Use

- Status: `IN_REVIEW / Proposed`. This file is a reviewable UI capability/route overlay for the user-approved roadmap direction; it is not yet an approved design authority and cannot authorize implementation or acceptance.
- The external Phase 1 UIUX package remains the unchanged approved complete-V1 superset. If this matrix receives explicit overall human approval, it will govern first-due timing and visible capability without rewriting package history or reducing the final V1.2 result. Until then, conflicts remain gated by `../governance/EVIDENCE_POLICY.md` and `../intake/V1_PACKAGE_INTAKE.md`.
- V1.1 is cumulative over V1.0 and V1.2 is cumulative over V1.1. An earlier formal object remains readable and immutable after a later capability is introduced.
- This is a UI capability contract, not an API, schema, feature-flag, or deployment contract. The server remains authoritative for the actor, object, revision, business guard, and allowed action.
- [System Degradation and Recovery UIUX](SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md) is the proposed common presentation contract when an introduced capability is partially unavailable, stale, retry-limited, or recovering. Release capability and runtime degradation are independent: a degraded state cannot introduce a later-release action, and a release state cannot relabel stale data as current.
- V2.0 financial research requires a separate PRD, UIUX package, route matrix, scenario inventory, and acceptance set. No novel surface below is a financial UI contract.

## Capability States

| State | Navigation and presentation | Action rule |
|---|---|---|
| `Enabled` | Present in ordinary navigation and eligible deep links | The authoritative capability still decides enabled/disabled and returns every reason |
| `Scoped` | Present only for the named workload/subpage in this release | No other workload can reuse the route merely because the shell exists |
| `Read-only history` | Existing authorized artifacts remain readable but no new artifact of that type can be created | Mutation and AI execution are absent or disabled with the exact reason |
| `Not introduced` | Absent from ordinary navigation, Bot actions, pending/activity entries, and export choices | Direct/stale deep links render `当前版本未启用` plus current release, requested capability, safe return, and preserved `returnTo`; they never fall through to another action |
| `Unknown/stale` | Preserve already loaded authorized data and navigation context | Fail closed for all writes and AI execution until capability refresh succeeds |

`Not introduced` is different from a business-state block. A later-release action must not appear as though completing a form, changing role, or retrying will unlock it. A present-but-blocked action remains discoverable and explains the current task/object blockers.

`Enabled` also does not mean currently healthy. An introduced capability can be temporarily degraded; its page still consumes server-authoritative `degradationMode`, `affectedCapabilities`, `dataFreshness`/`asOf`, `retryable`/`retryAfter`, and optional verified `lastKnownGoodRef`. Unknown degradation/freshness fails closed for writes and AI without changing the release introduction state.

## Page and Route Matrix

| Surface | V1.0 — 小说场景 | V1.1 — 内容分析与运营复盘 | V1.2 — 创作与运营闭环效果 |
|---|---|---|---|
| AUTH | `Enabled`: login, first password change, lockout, session recovery | Cumulative | Cumulative |
| P01 work home | `Enabled`: current-release Bot/deterministic entries, continue, pending, complete task list | Cumulative; may route to due release/feedback/analysis work | Cumulative; may route to next-round/comparison/value work |
| Stage 0 | `Scoped`: confirm and version `CreationBaseline` for initial creation | `Scoped`: before release readiness, confirm/version the additional `OperationValidationBaseline`; never silently backfill or rewrite V1.0 | Cumulative; a material baseline change shows comparison/Cycle impact and restarts the consecutive-validation baseline where required |
| P02 dashboard | `Enabled`: creation state, blockers, formal snapshot, V1.0 completion, current-release one next action | Cumulative; first-release, observation, formal-analysis, decision, and one-Cycle outcome states | Cumulative; decision-driven next round, adjacent-Cycle result, value state, and following Cycle N+2 entry |
| P03 studio | `Enabled`: references, initial creation, candidate compare/edit, Review, formal content, memory, versions | Cumulative: every V1.0 creation/edit/Review/formal capability remains enabled; this proposed matrix adds only the V1.1 packaging handoff. Feedback-driven next-round creation remains `Not introduced` until V1.2 | `Scoped`: formal V1.1 decision can create a bounded next-round plan/input and new candidate; lineage to new formal version is visible |
| P04 release/feedback | `Not introduced` | `Enabled`: packaging/release plan, manual actual release, external events, feedback/correction, first valid Cycle | Cumulative; second and later releases/Cycles remain bound to the decision-driven version |
| P05 analysis/decision | `Not introduced` | `Scoped`: analysis and decision subpages, including evidence insufficiency, continue observing, formal analysis, and formal human decision | Cumulative |
| P05 next-round/comparison/value | `Not introduced` | `Not introduced`; the V1.1 one-Cycle outcome points to its available completion/next-safe state without exposing these controls | `Enabled`: next-round plan, comparable/partially comparable/not-comparable views, two-Cycle value result, and following Cycle N+2 path |
| Agent execution trace | `Enabled` for actual V1.0 creation roles/models/attempts | Cumulative for analysis and packaging workloads | Cumulative for decision-driven creation; topology remains read-only |
| Global Bot/Agent/pending/settings/activity | `Enabled` only for current-release targets | Cumulative; newly introduced P04/P05 targets appear only after release capability refresh | Cumulative; next-round/comparison/value targets appear only when introduced |
| A01–A04, A06–A08 | `Scoped` to identity, creation scene/roles, approved models/cost, compliance, execution monitoring, and audit due in V1.0 | Cumulative with platform/metric/analysis workload records | Cumulative with decision-driven creation/comparison records |
| A05 Prompt governance | `Enabled` as controlled `PromptConfigBundle`/`EvaluationBinding`/safe `ExecutionBinding` registry, evaluation, promotion, ExplicitPilot/Shadow, revoke, first-version no-AI fallback, and later-version rollback for every Prompt used by V1.0 | Cumulative with separately evaluated V1.1 families/workloads | Cumulative with separately evaluated V1.2 families/workloads; no prior evaluation is inherited across a changed PromptConfig/Evaluation binding |
| System degradation/recovery presentation | `Scoped` horizontally when affected: AC-26A on shared shell, P01, Stage 0, P02, P03, A05, V1.0 D11, and all five operation classes | Cumulative H0 regression plus AC-26B on P04/P05, D04-D09, release/feedback/analysis/decision and D12 reconciliation | Cumulative H0/H1 regression plus AC-26C on next-round, comparison/value, following Cycle N+2, complete export and D12 simple survey |

## Dialog and Action Matrix

| Dialog/action | First due | Release-scoped rule |
|---|---|---|
| D01 AI execution preview | V1.0 | V1.0 initial creation only; V1.1 adds packaging/analysis; V1.2 adds decision-driven creation. A later workload is `Not introduced`, not a selectable disabled option |
| D02 formal content/packaging | V1.0 | Content confirmation is due in V1.0; packaging mode is introduced in V1.1 |
| D03 important-risk acceptance | V1.0 | Applies only where the current-release Review permits risk acceptance; compliance blocks never expose it |
| D04 actual release | V1.1 | Not reachable in V1.0; remains manual external-release confirmation |
| D05 external event | V1.1 | Not reachable without an eligible actual release/Cycle |
| D06 feedback snapshot | V1.1 | Not reachable in V1.0; correction preserves old snapshots and stales dependent analysis |
| D07 formal analysis | V1.1 | Decision candidates or model recommendations do not bypass this owning confirmation |
| D08 human decision/continue observation | V1.1 | Continue observing is a separate mode and not a formal `HumanDecision`; effective/invalid/terminal outcomes retain their distinct guards |
| D09 replacement decision | V1.1 | Only after an eligible formal decision; replacement history is immutable. Any V1.2 downstream plan stays blocked until revalidated |
| D10 task control | V1.0 | Desktop/compact-workspace only. Pause, resume, terminate, archive, restore, and delete are all disabled at `0–767px`; there is no mobile resume exception |
| D11 export | V1.0 | V1.0 content package; V1.1 operational review package; V1.2 complete lineage package. Mobile may preview/download an already generated authorized package but cannot configure or generate it |
| D12 Cycle time and value collection | V1.1 / V1.2 | `cycleTimeReconciliation` is first due on desktop/compact workspace after every ended Cycle in V1.1, including a Cycle N that may later become the first member of the valid pair; it remains a complex mobile-prohibited action. V1.2 adds `twoCycleSurvey` after the adjacent valid Cycle N+1; only that simple survey is the package-defined mobile write exception |
| Common degraded recovery | H0 / V1.0 | Exactly one primary CTA remains. A safe normal action keeps priority and retry stays secondary; otherwise one authoritative refresh/compare/receipt/manual recovery replaces it. No automatic formal-write, paid-AI, model-switch, object-finalize, or unknown-outcome replay; H1/H2 regress the rule on each newly introduced dialog/action |

## Decision-Candidate Placement

`DecisionCandidatePanel` renders an untrusted `SemanticFindingCandidate` as a reusable region inside the owning page, never a global decision center or first-level route. It keeps model status (`candidate`, `abstain`, `needs_human_review`) separate from authoritative deterministic-validation or compliance-policy blocks.

| Release | Owning surface examples | Required presentation |
|---|---|---|
| V1.0 | P01/Stage 0 intent or field clarification; P03 reference risk, Review, memory/change questions | Candidate question/version, input version, evidence/counterevidence, contradictions, gaps, risks, alternatives, abstention/human-review state |
| V1.1 | P04 release-difference/external-event/evidence triage; P05 analysis and action options | Fact/interpretation separation, exact evidence locators, counterevidence/confounders/unknowns, no-causality language, human-review reasons |
| V1.2 | P05 next-round/change-impact/comparison; P03 bounded decision-driven plan | Formal decision lineage, allowed action set, out-of-scope change, comparison limits, evidence insufficiency, and conservative conflict handling |

If a deterministic rule returns one legal next action, that action remains the page's only primary action and the panel is secondary. If several legal low-risk actions remain, the only primary action is `审阅并选择下一步`; selecting an option does not mutate state and the owning formal flow still revalidates capability.

## Responsive Capability Matrix

| Width | Layout | Allowed | Disabled or constrained |
|---|---|---|---|
| `1440+` | Wide desktop, fixed secondary context where specified | All authorized desktop capabilities | None solely because of width |
| `1280–1439` | Desktop with overlay secondary context | All authorized desktop capabilities; formal state and primary action remain visible | No critical information may exist only behind an unannounced overlay |
| `768–1279` | Compact workspace: single-column sections or one exclusive full-height overlay for navigation, evidence, comparisons, tables, drawers, and dialogs | Authorized desktop capabilities normally remain available, including A05, subject to ordinary role/business guards | No hover-only action, clipped evidence, missing hidden-column detail, or silent mobile fallback. A formal action whose complete preview cannot be safely presented fails closed with an explicit 1280 × 720 requirement and never submits reduced fields |
| `0–767` | Mobile read-only business renderer | Login/session recovery; navigation; task/status/formal-content reading; authorized Bot history; read-only Agent timeline; read-only decision evidence; D11 existing-package preview/download; D12 simple survey | Bot input/action apply, candidate adoption/comparison, human-review completion, AI execution, formal mutation, release, decision, all D10 modes including resume, admin, D11 configuration/generation, and D12 complex reconciliation |

The 767/768 and 1279/1280 boundaries are official-Web acceptance boundaries. The renderer must fail closed for the prohibited action and a short-lived presentation reference prevents stale submission after route/layout changes; the server separately enforces normal role, ownership, revision, policy, and business guards. Viewport, User-Agent, a client-supplied mode, and the presentation reference are not device attestation and cannot prove physical screen width. This release therefore claims official-Web responsive conformance, not prevention of a non-official client claiming desktop mode; a universal device restriction would require a separately approved managed-client/attestation contract.

## Versioned Behavior and Visual Evidence Gate

- The package contains 130 continuous scenarios: 55 `exact` and 75 `representative`. Every scenario requires a behavior assertion; representative or generic-template references do not prove page-specific visuals.
- First-due grouping is by primary outcome, not an automatic assignment of every assertion inside a numeric range: scenarios 1–64 primarily cover V1.0 creation; 65–99 primarily cover V1.1 release/feedback/analysis/decision; 100–106 and 129–130 primarily cover V1.2 next-round/comparison/value. Any assertion naming a surface not yet introduced is first due with that surface. Scenarios 107–128 are horizontal/admin capabilities first exercised on their V1.0 scope and expanded/retested on every newly introduced V1.1/V1.2 surface named by that scenario.
- A release test manifest records every scenario and independently scoped subassertion as `introduced`, `required`, `regression`, or `N/A` with reason. Numeric grouping alone never waives or prematurely passes a later-release surface.
- Existing package visuals include only two 1280 and two 390 images. They cannot prove every route, dialog, DecisionCandidatePanel state, A05 lifecycle, compact-workspace layout, or phased-release completion state.
- After overlay approval, each release critical path needs exact visuals approved by the design owner for default, blocked/stale/degraded, candidate/formal, and release-completion states. V1.0 includes creation, DecisionCandidatePanel review, and AC-26A operation-class recovery; V1.1 includes P04/P05, one-Cycle outcome, and AC-26B; V1.2 includes all three comparability states, value result, the following Cycle N+2 entry (Cycle 3 on the normal 1→2 path), and AC-26C; A05 includes evaluation, approval, ExplicitPilot/Shadow, activation, revoke, first-version no-LKG fallback, and later-version rollback.
- Visual evidence covers the applicable package baseline at 1440 × 900, desktop at 1280 × 720, one recorded representative width within 768–1279, and mobile at 390 × 844. Boundary behavior at 767/768 and 1279/1280 is behavioral evidence even when no boundary screenshot is designated.
- Missing design, tooling, implementation, or execution evidence is `Unverified`, never Passed. Novel behavior/visual evidence cannot satisfy V2.0 financial acceptance.

## System Degradation First-Due Registry

This registry adds cross-scenario subassertions; it does not change the external package's 130 scenario titles, `exact`/`representative` counts, or evidence. Every row is `IN_REVIEW / Proposed`, and all exact/behavior results remain `Unverified`.

| Gate | AC child | Minimum package scenarios whose due surface must add the common degradation assertion | Required behavior evidence | Exact/behavior status |
|---|---|---|---|---|
| H0 / V1.0 | AC-26A | 4, 7, 17–21, 29–45, 50, 64, 107–128 | Common fields; draft/formal-write/read-only-query/AI/object safety split; 429/503 bounded retry; local/server save labels; receipt-first unknown result; one CTA; 390 mobile prohibition and D11 limit; accessible scope/freshness/recovery | `Unverified` |
| H1 / V1.1 | AC-26B | H0 set as regression plus 65–99 and 129 where the named P04/P05/D04-D09/D12 surface is due | External-fact freshness and `asOf`; partial failure isolation; feedback preservation; no stale analysis/release/decision; retry cannot duplicate release/Cycle/formal decision | `Unverified` |
| H2 / V1.2 | AC-26C | H0/H1 sets as regression plus 100–106 and 130 | Decision lineage and prior-Cycle freshness; comparison/value stale states; following Cycle N+2 remains blocked on unknown authority; complete-export object failure; D12 local preservation without unauthorized mobile submit | `Unverified` |

The release test manifest expands these IDs into route, viewport, actor, operation class, dependency condition, field values, primary/secondary action, focus/announcement, and evidence reference. A later H1/H2 result cannot retroactively qualify H0, and an existing package `exact` screenshot cannot prove a newly proposed degradation state.

## Scenario-by-Scenario First-Due Registry

本表逐项登记外部 `state_matrix.json` 的 1–130 场景，解决仅按区间推断造成的歧义。它仍是 `IN_REVIEW / Proposed`：`First due` 是该场景最早可验收的当前版本子断言，不代表尚未启用 surface 已提前通过；`Later qualification` 是强制回归/扩展责任，不能省略。每个 release test manifest 仍须把场景内各 subassertion 展开到 route、viewport、actor、state、action 和 evidence ref。

| ID | Package scenario | Package coverage | First due | Later qualification |
|---:|---|---|---|---|
| 1 | 普通登录 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 2 | 首次登录强制改密 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 3 | 登录失败与账号锁定 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 4 | 会话过期后重新登录并恢复草稿 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 5 | 工作主页首次进入／空任务、筛选无结果及正常回流 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 6 | 结构化开始任务 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 7 | 主页 Bot 辅助开始或继续任务：无任务、多任务选择、意图歧义、上下文切换、动作卡、草稿预览、全局执行占用、失败降级和动作卡过期 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 8 | 阶段 0 独立业务路由、分步草稿、浏览器返回和主页状态恢复 | `exact` | V1.0（Creation 子断言） | V1.1 OperationValidation 扩展首次到期；V1.2 累计回归 |
| 9 | 阶段 0 缺失必填和动态核验 | `exact` | V1.0（Creation 子断言） | V1.1 OperationValidation 字段/动态核验首次到期；V1.2 累计回归 |
| 10 | 阶段 0 确认与冻结影响 | `exact` | V1.0（Creation 子断言） | V1.1 OperationValidation 独立确认/冻结/替换影响首次到期；V1.2 累计回归 |
| 11 | 从主页前往 P02 后执行任务暂停和恢复 | `exact` | V1.0 | V1.0 行为到期；D10 专项视觉仍须新增，V1.1/V1.2 回归 |
| 12 | 从主页前往 P02 后执行全局终止 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 13 | 从主页前往 P02 后执行归档和恢复归档 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 14 | 从主页前往 P02 后执行删除二次确认 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 15 | 无创作参考 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 16 | 粘贴文本 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 17 | 文件上传和处理中 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 18 | 可用资料 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 19 | 部分可用 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 20 | 处理失败 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 21 | 文件或任务超限 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 22 | 权利不明确禁止生成 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 23 | 本次引用选择 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 24 | 实际使用来源定位 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 25 | 停用和归档 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 26 | 删除被候选使用的资料 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 27 | 删除影响正式内容的资料 | `representative` | V1.0 | V1.0 验 P03 子断言；P04 子断言 V1.1 首次到期；V1.2 回归 |
| 28 | 资料提示诱导风险 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 29 | 正常执行预览 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 30 | 黄色模型政策逐次确认 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 31 | 红色模型政策阻断 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 32 | 全局已有执行时排队 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 33 | 排队前取消 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 34 | 排队期间输入变化后重新预览 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 35 | 三模型并行运行 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 36 | 后台运行后返回页面 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 37 | 预算 80% 预警 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 38 | 预算 100% 阻断 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 39 | 部分完成 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 40 | 模型失败 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 41 | 重试形成新尝试 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 42 | 换模型形成新尝试 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 43 | 暂停后续步骤 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 44 | 恢复同一输入 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 45 | 输入变化后无法恢复旧执行 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 46 | 候选切换和并排比较 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 47 | 设置主候选 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 48 | 人工编辑形成新候选 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 49 | 废弃与保留候选 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 50 | 上游变化导致候选过期 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 51 | 六维 Review | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 52 | 建议问题 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 53 | 重要风险带理由继续 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 54 | 阻断问题 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 55 | 合规阻断 | `representative` | V1.0 | V1.0 验 P03 子断言；P04 子断言 V1.1 首次到期；V1.2 回归 |
| 56 | Agent 分歧卡和人工裁决 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 57 | 作品事实冲突 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 58 | 正式内容确认 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 59 | 记忆变化确认 | `exact` | V1.0 | V1.1/V1.2 累计回归 |
| 60 | 记忆待确认导致不可投放 | `exact` | V1.0 | V1.0 验 P03 子断言；P04 子断言 V1.1 首次到期；V1.2 回归 |
| 61 | 新完整内容快照 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 62 | 查看和比较正式快照 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 63 | 基于旧快照创建候选 | `representative` | V1.0 | V1.1/V1.2 累计回归 |
| 64 | 上游正式变化导致下游重审 | `exact` | V1.0 | V1.0 验 P03 子断言；P04 子断言 V1.1 首次到期；V1.2 回归 |
| 65 | 包装 AI 候选 | `representative` | V1.1 | V1.2 累计回归 |
| 66 | 包装人工候选 | `representative` | V1.1 | V1.2 累计回归 |
| 67 | 包装 Review 与正式版本 | `representative` | V1.1 | V1.2 累计回归 |
| 68 | 发布计划草稿 | `exact` | V1.1 | V1.2 累计回归 |
| 69 | 投放前检查中 | `representative` | V1.1 | V1.2 累计回归 |
| 70 | 平台规则未配置／已过期 | `representative` | V1.1 | V1.2 累计回归 |
| 71 | AI 标识待人工核验 | `representative` | V1.1 | V1.2 累计回归 |
| 72 | 具备手工投放条件 | `exact` | V1.1 | V1.2 累计回归 |
| 73 | 记录已提交／审核中 | `representative` | V1.1 | V1.2 累计回归 |
| 74 | 正常实际投放确认 | `exact` | V1.1 | V1.2 累计回归 |
| 75 | 实际与计划轻微差异 | `representative` | V1.1 | V1.2 累计回归 |
| 76 | 实际与计划实质差异 | `exact` | V1.1 | V1.2 累计回归 |
| 77 | 平台驳回或投放失败 | `representative` | V1.1 | V1.2 累计回归 |
| 78 | 外部失效或平台下架 | `representative` | V1.1 | V1.2 累计回归 |
| 79 | 活跃 Cycle 中轻微修改 | `representative` | V1.1 | V1.2 累计回归 |
| 80 | 活跃 Cycle 中实质修改 | `exact` | V1.1 | V1.2 累计回归 |
| 81 | 用户绕过合规阻断投放 | `representative` | V1.1 | V1.2 累计回归 |
| 82 | 发布记录有限更正 | `representative` | V1.1 | V1.2 累计回归 |
| 83 | 24h 反馈草稿和确认 | `exact` | V1.1 | V1.2 累计回归 |
| 84 | 72h 与 7d 多快照 | `exact` | V1.1 | V1.2 累计回归 |
| 85 | 数值、真实为 0、不可用、不适用和未填写 | `exact` | V1.1 | V1.2 累计回归 |
| 86 | 评论粘贴与隐私提示 | `exact` | V1.1 | V1.2 累计回归 |
| 87 | 截图证据与不发送模型提示 | `exact` | V1.1 | V1.2 累计回归 |
| 88 | 暂停期间补录反馈 | `representative` | V1.1 | V1.2 累计回归 |
| 89 | 反馈更正导致分析失效 | `representative` | V1.1 | V1.2 累计回归 |
| 90 | Cycle 结束后的迟到反馈 | `representative` | V1.1 | V1.2 累计回归 |
| 91 | 证据不足分析 | `exact` | V1.1 | V1.2 累计回归 |
| 92 | 初步分析 | `exact` | V1.1 | V1.2 累计回归 |
| 93 | 正式分析候选与人工确认 | `exact` | V1.1 | V1.2 累计回归 |
| 94 | 分析过期 | `representative` | V1.1 | V1.2 累计回归 |
| 95 | 继续观察并增加时间点 | `representative` | V1.1 | V1.2 累计回归 |
| 96 | 正式人类决策 | `exact` | V1.1 | V1.2 累计回归 |
| 97 | 本轮结束后暂停 | `representative` | V1.1 | V1.2 累计回归 |
| 98 | 本轮结束后结束作品迭代 | `representative` | V1.1 | V1.2 累计回归 |
| 99 | 替代决策 | `representative` | V1.1 | V1.2 累计回归 |
| 100 | 下一轮方案候选和确认 | `exact` | V1.2 | V1.2 首次完整验收 |
| 101 | 下一轮执行中无活跃 Cycle | `representative` | V1.2 | V1.2 首次完整验收 |
| 102 | Cycle 1 与 Cycle 2 可比 | `representative` | V1.2 | Package 标题保留正常路径示例；权威行为参数化为首个相邻有效对 N/N+1 |
| 103 | 部分可比 | `exact` | V1.2 | V1.2 首次完整验收 |
| 104 | 不可直接比较 | `representative` | V1.2 | V1.2 首次完整验收 |
| 105 | 两轮机制与价值验证结果 | `representative` | V1.2 | V1.2 首次完整验收 |
| 106 | 开始 Cycle 3 | `representative` | V1.2 | Package 标题保留正常路径示例；权威行为进入首个相邻有效对后的 Cycle N+2 |
| 107 | Bot 解释和应用草稿预览 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 108 | Bot 跳转正式操作 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 109 | Agent 协作执行详情 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 110 | 待处理阻断深链 | `representative` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 111 | 高级设置只影响未来执行 | `representative` | V1.0 | 高级设置只改基线边界内的未来偏好；扩大模型/语言/预算/权利边界必须替换基线；D01/ExecutionBinding 固化实际值，V1.1/V1.2 累计回归 |
| 112 | 活动弹层的运行、完成、失败和未读 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 113 | 后台模型异常 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 114 | 后台模型政策降级 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 115 | 后台规则版本生效 | `representative` | V1.0 | V1.0 验当前治理范围；V1.1 平台/分析规则扩展；V1.2 回归 |
| 116 | 管理员终止异常执行 | `representative` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 117 | 管理员调试查看及审计 | `representative` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 118 | 三类导出包选择 | `representative` | V1.0（子断言） | V1.0 内容包；V1.1 单 Cycle 包；V1.2 三类包完整 |
| 119 | AI 标识和导出范围预览 | `representative` | V1.0（子断言） | 随 V1.1/V1.2 新增导出范围扩展并回归 |
| 120 | 导出生成中、完成和失败重试 | `representative` | V1.0（子断言） | 随 V1.1/V1.2 新增导出范围扩展并回归 |
| 121 | 自动保存中、成功和失败 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 122 | 离线编辑与恢复同步 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 123 | 页面版本过期 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 124 | 长任务 30 分钟超时并保留部分结果 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 125 | 1280 宽度适配 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 126 | 移动端只读 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 127 | 桌面端继续提示 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 128 | 任务切换时抽屉关闭与上下文清理 | `exact` | V1.0 | 随 V1.1/V1.2 新增 surface/workload 重新限定并回归 |
| 129 | 每个 Cycle 结束后的主动协调时间核对 | `representative` | V1.1（每个已结束 Cycle） | V1.2 对构成首个相邻有效对的 Cycle N/N+1 完成两次汇总；每个后续 Cycle 均回归 |
| 130 | 第二个连续有效 Cycle 后的价值问卷和未完成状态 | `representative` | V1.2 | V1.2 首次完整验收 |

`exact` 只表示现有截图直接覆盖 package 所述核心状态，不代表分版新增状态、替代 viewport、A05 新生命周期或 DecisionCandidatePanel 已有视觉证据；`representative` 必须补行为证据，关键路径还须按上文 Gate 补专项 exact 视觉。
