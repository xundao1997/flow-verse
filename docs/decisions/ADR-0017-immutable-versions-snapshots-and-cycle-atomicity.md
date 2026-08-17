# ADR-0017: 不可变版本、Snapshot 与 Release/Cycle 原子性

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../product/V1_PRODUCT_BRIEF.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/RELIABILITY_BUDGET.md`；`ADR-0024-cumulative-release-capability-activation.md` |
| Supersedes | N/A |

## Context

- AI 只产生候选；用户确认后才形成正式内容、记忆、分析和决定。
- 外部发布必须绑定精确内容/包装/章节/平台/账号，且确认实际生效与创建 Cycle 必须全成或全不成。
- 更正要保留旧值、传播 stale，不允许覆盖历史或重排 Cycle 编号。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 不可变版本 + manifest snapshot + 原子状态事务 | 可复现、可审计、易判断 stale | 版本/存储增长与查询复杂度 | Medium | 当前候选 |
| B. 就地覆盖 current row | CRUD 简单 | 历史、引用、恢复和外部事实不可证明 | Low | 无正式性/审计要求时 |
| C. 全量 event sourcing | 完整事件历史 | 投影、迁移、团队复杂度过高 | High | 多消费者/重放需求被证明后 |

## Decision

- Proposed option A：draft 可修订；candidate 和 FormalVersion、MemoryVersion、Snapshot、FeedbackSnapshot、FormalAnalysis、HumanDecision 均采用不可变版本或 append-only replacement chain。
- 正式命令在一个 PostgreSQL 事务内重验 owner/revision/capability/policy，创建 formal object + immutable manifest + audit/receipt；失败不产生部分正式事实。
- Snapshot 固定内容/包装/章节/记忆/参考与 object hash/config refs；不得通过“current”指针重解释历史。
- `ActualRelease + ReleaseCycle` 原子创建；一个 task 最多一个 active Cycle；Cycle number 单调且无效后不重排。
- 更正创建新记录，旧依赖确定性 stale；正式决定可被替代但不覆盖。V1.2 使用首个相邻有效 N/N+1 对，N+2 是后续入口。
- append-only audit 不是通用 event sourcing；业务当前状态仍由 owner 表和明确投影维护。

## Rationale and Trade-Offs

- 不可变 manifest 是 Prompt、发布、恢复和复盘可复现的共同基础。
- 接受存储增长与版本查询成本；通过 retention、分页、正文按需、投影可重建缓解。
- 不引入完整 event-sourcing 基础设施，保持事务模型可理解。

## Impact

- PostgreSQL 是版本/指针/唯一约束 authority；ObjectStore 对象版本由 hash/locator 引用。
- 删除、导出与恢复必须遍历版本引用并防复活；缓存不能成为 current pointer authority。
- 正式命令、更正、Cycle/价值评估需要并发与 property/integration 测试。

## Implementation and Verification

- DB 约束覆盖 current pointer、replacement chain、one-active-cycle、编号、candidate/formal 分离和原子 release。
- 测试并发确认、重复 command、保存失败、部分对象失败、stale propagation、无效 Cycle 和 restore 后唯一性。
- 历史快照 diff/hash 与当时 binding/config/evidence 可定位，缺一不可标可复现。

## Revisit Triggers

- 版本增长影响批准性能、第二消费者需要事件订阅、审计重放成为法律要求，或跨服务提取发生。

