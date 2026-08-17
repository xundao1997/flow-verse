# ADR-0012: Public API、正式命令、收据与降级合同

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/V1_FRONTEND_TECHNICAL_DESIGN.md`；`../uiux/INTERACTION_RULES.md`；`../uiux/ACCEPTANCE_CRITERIA.md` |
| Supersedes | N/A |

## Context

- FlowVerse 区分 query、普通 draft mutation 和产生正式事实/费用/外部副作用的 command。
- 网络结果未知、重复提交、旧 revision、依赖降级和陈旧只读结果必须可恢复，不能靠文案猜测。
- 当前只实现 operational endpoint；业务 OpenAPI、auth 和错误协议均未获批。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. REST resource + 显式 command/receipt | 语义清楚、可幂等与审计、便于生成客户端 | 合同较多，需要状态/错误测试 | Medium | 当前候选 |
| B. 通用 mutation/execute endpoint | 表面简洁 | 隐藏领域语义、权限与副作用，无法稳定兼容 | Low initially | 不满足正式性要求 |
| C. GraphQL 全面替代 | 查询灵活 | command/idempotency/缓存/错误仍需另建 | Medium-high | 多复杂查询消费者被证明后 |
| D. 延后 | 不提前锁协议 | 业务实现保持阻断 | Low now | Schema/auth 未决时 |

## Decision

- Proposed option A：业务 public API 使用版本化 REST/OpenAPI；public 与 `/internal/v1` 身份、网络和预算分离。
- query 返回 resource revision、capability 与 freshness；draft mutation 使用 `expectedRevision`；正式 command 使用稳定 `commandId`、Idempotency-Key/digest、target scope、D2 重验与不可变 receipt。
- 响应丢失时允许当前 actor 通过 `commandId` 定位同一 receipt；幂等 retention/expiry 到期后不得静默重放未知副作用。
- 统一错误/降级 envelope 至少包含稳定 code、preserved、recoveryActions、`degradationMode`、`affectedCapabilities`、`dataFreshness/asOf`、`retryable`、`retryAfter` 与适用的 `lastKnownGoodRef`。429/503 同步 HTTP `Retry-After`。
- 未知 enum/code fail safe；Web 只执行服务端允许的有界重试，正式 command 不自动重试。

## Rationale and Trade-Offs

- 显式命令把人类确认、revision、权限和副作用放在可测试边界。
- 接受 endpoint 数量和客户端生成成本，换取兼容、恢复与审计。
- 降级元数据可能增加响应体；只返回低基数、最小必要状态，不泄露内部拓扑或敏感错误。

## Impact

- OpenAPI 是 public contract 唯一生成源；前端不得复制业务 enum/状态机。
- 保存草稿、正式写、只读查询、AI 候选和对象 grant 分别定义 fail-open/fail-closed。
- additive expand/contract 为默认兼容策略；破坏性协议变化另起 major/ADR。

## Implementation and Verification

- 契约测试覆盖 duplicate、stale、outcome-unknown、receipt lookup、429/503、陈旧读和未知 code。
- E2E 验证用户能看到工作是否保存、数据时点、受影响能力和唯一下一步；无界 retry/storm 测试必须失败。
- 未批准 auth/Schema/retention 和精确 HTTP 细节前不得生成业务 OpenAPI。

## Revisit Triggers

- 出现第二类 public client、离线同步需求、破坏性兼容需求，或 REST 聚合查询成为有证据的瓶颈。

