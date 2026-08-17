# ADR-0015: S3 ObjectStore 合同、对象状态机与 MinIO adapter

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-SERVER-MIDDLEWARE-DEPLOY / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/TECH_STACK.md`；`../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`ADR-0018-cross-store-recovery-and-deletion-ledger.md` |
| Supersedes | N/A |

## Context

- 当前单机 MinIO 仅是已配置能力：无业务 bucket/account/adapter，live auth 仍 Unverified，不能证明 TLS、备份、恢复或 HA。
- V1 需要保存参考原件、截图证据、执行 delivery 和导出二进制；正文、正式版本、权限和状态仍由 PostgreSQL 权威拥有。
- 生产存储厂商、区域、成本、许可和故障域尚未批准。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 窄 S3 contract + 可替换 adapter | 开发可用 MinIO，生产可按证据选托管/自建 | 需要严格子集和合同测试 | Medium | 当前候选 |
| B. 将字节存入 PostgreSQL | 单事务简单 | 大对象、备份、IO 和传输压力 | Low initially | 仅很小且低量对象 |
| C. 业务直接绑定 MinIO SDK/路径 | 快速 | root/bucket/key/供应商语义泄漏，难迁移 | Low initially | 不满足可替换要求 |
| D. 多云抽象平台 | 迁移能力强 | 当前无第二消费者，过度设计 | High | 实际多区域/多供应商要求批准后 |

## Decision

- Proposed option A：定义最小 `ObjectStore` port，仅覆盖 create upload grant、finalize、head/hash、server-side copy/commit、read grant、delete/version listing 和 recovery enumeration 所需 S3 子集。
- PostgreSQL 保存 logical object/version、opaque locator、expected size/type/hash、rights、purpose、state 和引用；浏览器与业务领域不能构造 bucket/key。
- 状态固定为 upload/quarantine/verify/process/commit/delete 链。`VERIFIED` 只允许受控解析；`PROCESSING/PARTIAL` 不可下载或进 manifest；仅 `COMMITTED` 可按 actor/owner/purpose授权。
- finalize 后由服务端验证实际 MIME、size、hash、session/locator；参考内文本是 untrusted data，截图禁止入模。
- 当前 MinIO 只作为开发 adapter。业务启用前必须修复 live auth，创建最小权限应用 identity、用途隔离、TLS/加密、lifecycle/quota、backup/restore 和 contract suite。
- 生产在受维护的分布式 S3-compatible 实现与托管对象服务间另行批准；单机 MinIO/单卷不构成 durability 证据。

## Rationale and Trade-Offs

- 窄合同隔离供应商生命周期，同时不承诺虚假“数据库无关”。
- 接受 PG+ObjectStore 双存储恢复复杂度；由不可变对象、checkpoint 和独立 deletion ledger 缓解。
- 不提前实现多云复制；迁移以 shadow copy、hash、reference switch、rollback window 和删除对账完成。

## Impact

- 所有正式 snapshot/execution/export manifest 只引用 `COMMITTED` object version/hash。
- 依赖 ObjectStore 的 capability 可独立 fail closed；PG 中正文/任务/审计可按降级合同继续。
- 需要对象容量、保留、加密、访问日志和恶意文件 quarantine 监控，但不把高基数 locator/hash放 metric label。

## Implementation and Verification

- adapter contract 覆盖权限、过期 grant、错误 locator、MIME/hash 不符、部分上传、重复 finalize/delete 和 provider outage。
- integration/recovery 测试使用专用非 root identity 和隔离 bucket；验证备份、恢复、迁移与防复活。
- 未通过 live auth 与完整对象合同前，V1 参考/导出/正式对象 capability 保持禁用。

## Revisit Triggers

- 上游维护/许可变化、区域/驻留要求、容量/成本/RPO 变化、第二对象供应商或多区域恢复成为批准需求。

