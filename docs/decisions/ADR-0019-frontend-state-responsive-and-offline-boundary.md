# ADR-0019: 前端状态、响应式能力与离线边界

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../uiux/RELEASE_CAPABILITY_MATRIX.md`；`../uiux/INTERACTION_RULES.md`；`../engineering/V1_FRONTEND_TECHNICAL_DESIGN.md`；`../engineering/PERFORMANCE_BUDGET.md` |
| Supersedes | N/A |

## Context

- Desktop Web 是主端；390×844 业务只读，复杂创作、执行、确认、投放、决定和 admin 禁用，仅有命名的 D11/D12 窄例外。
- 当前 Web 只有诊断页；Router/query/form/editor/IndexedDB/E2E 依赖未批准。
- 服务器 capability 是授权权威，前端仍需守住布局能力、stale 状态和断网草稿。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. Feature slices + server state/query + local form/offline draft | 状态 owner清楚、可渐进实现 | 需要版本与恢复治理 | Medium | 当前候选 |
| B. 单一全局 store 承载所有状态 | 初期集中 | remote/form/capability互相覆盖、难失效 | Medium | 小型短生命周期 UI |
| C. 全离线同步 | 弱网体验强 | 冲突、权限、正式性复杂 | High | 明确多设备离线编辑需求后 |
| D. 仅 CSS 隐藏移动动作 | 简单 | API 可绕过、布局变化后能力失真 | Low | 不满足当前安全要求 |

## Decision

- Proposed option A：remote server state、URL state、form/editor state、local UI state 和受控 offline draft 分 owner；正式事实、capability 和 revision 不复制为客户端 authority。
- Router/query/form/editor/IndexedDB 等依赖必须精确锁版并进入 TECH_STACK；生成 API client 来自批准 OpenAPI。
- 官方 renderer 通过 `/capabilities` 获取短时 presentation capability ref；服务端命令仍独立重验角色、ownership、revision 和业务 capability。0–767 复杂动作 fail closed。
- IndexedDB 只保存用户明确编辑的加密/受控草稿和必要 metadata；localStorage/sessionStorage 不保存正文、token、Prompt、secret 或完整执行结果。
- SSE 是提示不是事实源；断线按 cursor 恢复，事件后 invalidate query。统一降级 UI 展示模式、受影响能力、freshness/asOf、工作是否保存、retry-after 和唯一恢复 CTA。
- GET/section 可有界重试；正式 command、付费执行和对象 finalize 不自动重试，先查 receipt/状态。

## Rationale and Trade-Offs

- 明确状态 owner 防止 stale 页面覆盖正式事实；服务端+presentation 双门满足移动安全。
- 接受多个前端状态层的学习成本；通过 feature slice、typed adapters 和测试矩阵控制。
- 不实现通用 offline-first，同步复杂性只在真实需求出现后增加。

## Impact

- Work home 的 Bot、continue、pending、task list 独立加载；Bot失败不阻断确定性入口。
- 每页一个主 CTA；SemanticFindingCandidate 只读展示证据/不确定性，人类在 owning page 提交。
- 前端性能必须按业务 bundle、长文、历史、SSE storm 和移动只读路径重新建基线。

## Implementation and Verification

- E2E/visual/a11y 覆盖 1440、1280、compact、767/768、390，包含 blocked/stale/degraded/offline/recovered。
- 测试 direct API bypass、presentation ref过期、SSE重连、receipt recovery、跨tab/刷新草稿、storage quota/清理和版本迁移。
- exact UIUX/工具/命令未批准时保持 Unverified，不以 representative screenshot 代替行为证据。

## Revisit Triggers

- 多设备同步、PWA/移动编辑、协作编辑、超大长文性能或第二前端客户端成为批准需求。

