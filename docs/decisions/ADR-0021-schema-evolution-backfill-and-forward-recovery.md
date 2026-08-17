# ADR-0021: Schema 演进、Backfill 与 Forward Recovery

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-ARCH-BASELINE / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/V1_DETAILED_TECHNICAL_DESIGN.md`；`ADR-0024-cumulative-release-capability-activation.md` |
| Supersedes | N/A |

## Context

- 当前 Alembic 只有空 Bootstrap migration；全部业务 DDL 都是 Proposed。
- V1.0～V1.2 累计激活要求混合版本、历史对象和回退时仍能安全读取。
- 大表、对象 manifest、Prompt binding 和删除/恢复不可通过破坏性数据库回滚重解释。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 单 head + expand/backfill/activate/contract | 可审计、支持混合版本与forward fix | 发布步骤与临时兼容成本 | Medium | 当前候选 |
| B. 每模块独立 migration head | owner自治 | 顺序/依赖/恢复复杂，易分叉 | High | 独立数据库服务后 |
| C. 直接修改/回滚 Schema | 快 | 锁表、数据丢失、旧制品误读 | Low initially | 仅无数据本地实验 |
| D. 永不删除旧列 | 回退容易 | 永久债务与双真相 | Low initially | 仅有明确长期兼容需求 |

## Decision

- Proposed option A：一个 API-owned Alembic head；每个 release 只实现批准物理 allowlist。
- 迁移序列为 expand → deploy compatible readers/writers → bounded backfill → validate/reconcile → activate capability → observe → contract。
- 大 backfill 使用 stable cursor、bounded batch、checkpoint、rate limit、pause/resume 和可重入 idempotency；不在 schema migration 事务内做远程/对象/模型调用。
- 新旧字段并存期指定唯一 write owner 和 read precedence；不得无限 dual-write 或让投影成为第二事实源。
- destructive contract 只在回退窗口、备份/restore 和引用检查通过后执行。越过不可逆点使用 forward recovery，不执行破坏性 down migration。
- Schema/version/config/object/recovery checkpoint 关联；restore 后运行 FK/UQ/hash/reference/ledger reconciliation。

## Rationale and Trade-Offs

- 单 head 与累计 capability 更匹配当前单数据库模块化单体，降低迁移竞态。
- 接受临时字段和分阶段发布成本，换取无停机演进与可验证回退。
- 具体 DDL、索引和批量大小必须由数据规模与计划证据决定，不在 ADR 中发明。

## Impact

- 每个 migration 有 owner、数据分类、锁风险、容量、forward/rollback plan 和 verification query。
- 读投影、continuous aggregate、向量/时序索引必须可重建，不作为正式 authority。
- 生产部署、activation 和 migration receipt 需要统一 release traceability。

## Implementation and Verification

- CI 检查单 head、upgrade from supported version、fresh install、mixed version、migration interruption/retry 和 schema drift。
- 代表性数据测试 lock time、WAL/IO、backfill rate、应用 P95 和磁盘 headroom；超过门则暂停。
- contract 阶段前完成 backup/restore、旧 artifact 回退测试与 owner sign-off。

## Revisit Triggers

- 模块拆独立数据库、表规模/迁移窗口改变、在线 Schema 工具需求、长期双版本客户端或跨区域复制出现。

