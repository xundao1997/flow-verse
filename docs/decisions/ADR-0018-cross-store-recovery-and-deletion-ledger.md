# ADR-0018: PostgreSQL 与对象存储一致恢复及防复活删除账本

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-13 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../intake/V1_PACKAGE_INTAKE.md` 中 `FV1-ROADMAP-REVIEW=IN_REVIEW`；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` 11.3～11.4、12.5～12.8、TD-17；`../engineering/RELIABILITY_BUDGET.md` Recovery Target Registry；`../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md` |
| Supersedes | N/A |

Allowed status values: Proposed, Accepted, Rejected, Deprecated, Superseded.

本 ADR 只是本轮同源文档变更的架构候选。它未获用户接受，也不证明备份、恢复、删除、RTO 或 RPO 已实现或通过验证。

## Context

- Problem: FlowVerse 的正式事实保存在 PostgreSQL，参考、截图、导出等二进制对象由 ObjectStore 承载。分别恢复“最近一次数据库备份”和“最近一次对象备份”可能产生缺失引用、错误对象版本、孤儿对象，或让已经删除的数据从旧备份中复活。
- Confirmed requirements: 正式记录不得因进程重启丢失；产品目标要求正式数据不丢失、草稿最多丢失 24 小时、RTO 4 小时；任务删除后内容按既定期限清理，备份按既定期限过期。具体故障包络及拓扑仍未获批准。
- Constraints: 当前 PostgreSQL、Redis、MinIO 只证明了服务端中间件准备状态；MinIO 尚无批准的业务 ObjectStore 合同；没有跨存储分布式事务、生产备份实现或恢复演练证据；恢复控制记录不能只依赖正在被恢复的 PostgreSQL 时间线。
- Current module/contract/data/reliability facts: PostgreSQL 是权威业务事实候选；对象必须通过 logical object ID、不可变 version/hash 和生命周期受控引用；Redis 不属于权威恢复集。精确 Schema、bucket、签名、保留周期和命令仍为 Unknown。
- Why a decision is required now: V1.0 的正式小说快照、V1.1 的投放/反馈证据和 V1.2 的跨 Cycle lineage 都可能同时依赖数据库与对象。若不先冻结一致恢复和防复活边界，备份存在也不能满足发布级恢复目标。

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| A. 分别备份并各自恢复 PostgreSQL 与对象存储 | 实现最简单；无需新增恢复清单 | 无法证明跨存储引用一致；删除数据可能复活；恢复结果不可重复验证 | Low | Low | 仅无跨存储正式引用且无删除/合规恢复要求时；不满足当前目标 |
| B1. Application recovery set：checkpoint epoch + PG MVCC consistent cut + 不可变分片manifest/Merkle + 独立ledger HWM | 快照可见集语义直接；可验证跨存储cut与防复活 | 必须避免无界长事务；需要有界物化、分片、对账和演练 | High | Low/Medium | 可在已批准窗口内有界物化MVCC可见引用集时 |
| B2. Application recovery set：单调object-reference commit watermark + 不可变分片manifest/Merkle + 独立ledger HWM | 不需长期持有MVCC事务；适合增长型对象引用集合 | 每次正式引用事务需分配watermark；必须证明无漏项/重号及cut语义 | High | Low/Medium | watermark可与正式引用原子提交并可恢复核验时 |
| C. 采用跨存储全局分布式事务 | 提交时一致性强 | 生态、可用性、性能和运维复杂度显著增加；仍不能替代备份与删除重放 | Very High | High | 有经验证的原子跨存储需求和平台能力时；当前无证据 |
| D. 延后正式对象存储与生产恢复 | 避免提前抽象 | 对象相关能力与生产发布必须保持阻断 | Low now | None | 不能及时确认恢复 owner、拓扑和证据时 |

## Decision

- Chosen option: **Proposed B-family，B1/B2 尚待 decision owner 二选一**。如本ADR被接受，每个可发布恢复点必须形成不可变application recovery set，并使用独立于业务PostgreSQL恢复时间线的append-only deletion ledger防止旧备份复活已删除数据；在consistent-cut算法、owner和演练被批准前，不得声称可恢复集合完整。
- Scope:
  - 对象写入采用 `quarantine → verified → committed` 候选生命周期；只有已验证的不可变 object version/hash 可在 PostgreSQL 事务中形成正式引用。数据库提交失败留下的对象保持不可见并由幂等对账清理。
  - `B1`在短事务中写checkpoint epoch并绑定PG timeline/LSN，以该epoch的PG MVCC可见集有界物化全部正式object-reference；manifest采用不可变分片与顶层Merkle root。不得为全量对象遍历持有无界长事务；具体snapshot/物化方式待数据owner批准。
  - `B2`要求每个正式object-reference在同一PG事务获得单调commit watermark；checkpoint选择`W`，只接受覆盖`<=W`且属于该恢复集合的不可变分片manifest/Merkle root。watermark唯一性、单调性、回滚/空洞语义和恢复后续号必须由约束与演练证明。
  - 两方案的recovery checkpoint都以受控root表达：`BUILDING → VERIFYING → RECOVERABLE`，构建/验证失败进入终态`FAILED`。cut identity从创建起不可改；进入VERIFYING前冻结一个strict、版本化且不可变的component manifest ref/hash，并把全部component refs纳入checkpoint hash/signature；只有PG cut、全部分片/Merkle/object coverage、当前ledger HWM、Schema/config、兼容应用制品、恢复步骤及各自signature/hash都通过才可进入RECOVERABLE。RECOVERABLE/FAILED后全字段不可变；同一版本不得修字段后重试，只能新建checkpoint。
  - component manifest至少绑定PostgreSQL恢复点及timeline/LSN、cut epoch或object-ref watermark、全部被纳入committed object的logical ID/version/hash/size、分片hash/Merkle root、对象备份或版本标记、deletion-ledger cursor/high-watermark、Schema version/ref/hash、配置ref/hash、compatible application artifact ref/hash，以及recovery procedure/runbook version/ref/hash；RECOVERABLE时这些字段不得为空或由可变“当前值”替代。
  - 删除使用 ledger-first 可重试状态机：先以稳定 commandId 向独立 deletion ledger 幂等追加最小化 delete intent，再在 PostgreSQL 事务中写不可访问 tombstone/pending receipt 和 ledger cursor；两边都耐久确认后才返回最终 receipt。账本不得与待恢复业务数据库共用同一 PITR 时间线、访问凭据和单一故障域；具体 WORM/append-only 实现待后续批准。
  - 若删除与在途Worker结果相交，ledger intent和PG tombstone耐久后必须先阻断该task的新job/input/call-start与普通DeliveryStore写grant，取消/fence相关WORK lease并停止续签/撤销`DELIVERY_BUFFER_CREATE`。唯一例外是barrier前已`CALL_START_COMMITTED`而尚未buffer的同一intent：API可签更高fencing的封闭`DELETION_DISPOSITION` lease与业务不可读`DELETION_DISPOSITION_BUFFER`单record grant，只能把既有outcome写入隔离区并报告discard，不能调用provider、读原输入或生成第二结果。等待全部pre-barrier intent进入buffered+receipted或耐久no-payload unknown，且普通/处置grant与专用lease收口后，才捕获unreceipted-index HWM、完整分页扫描到固定边界并复核无active producer、有效写grant或barrier后的迟到entry。对普通已`RESULT_BUFFERED`或处置隔离记录，API验证同一ledger intent、tombstone、job/context/result hash、原producer proof与`DELETION_DISPOSITION_LEASE|DELETION_RECONCILIATION` acceptance proof后写耐久`DISCARDED_BY_DELETION` receipt，而不创建output/candidate/artifact/formal事实；Worker只能凭该receipt安全擦除。任一barrier/index/HWM/处置证明不完整时`cleanupStatus`不得COMPLETE，不能靠TTL或容量压力丢弃。
  - 每个buffer写grant必须先耐久记录冻结预分配record/payload locator与envelope/result hash的`delivery-grant-intent/v1` receipt。无payload分支只有在全部相关lease/grant失效、逐个已签locator从未可见或已secure erase、固定index HWM完整无record且无并发处置后，API reconciliation才可写`NO_PAYLOAD_DISPOSITION_ACCEPTED`并把call/job置`OUTCOME_UNKNOWN_NO_PAYLOAD`；该proof仅说明本系统没有可恢复的本地payload，不证明provider未处理。任何孤儿locator或分页边界不可证时恢复/删除门保持关闭。
  - 恢复顺序为：恢复 PostgreSQL 与 checkpoint 指定对象版本；重放 deletion ledger 至已验证当前高水位；校验正式 hash/reference/唯一约束/待处理状态；全部门通过后才开放正式数据。
  - cut后新增引用不得误入checkpoint；cut后删除必须由ledger重放防复活。缺失分片/对象、Merkle/hash/version不符、PG cut不一致、账本覆盖不完整或当前高水位不可证时，受影响capability必须fail closed；Redis只重建，不作为权威恢复来源。
  - 当前MinIO只证明过单主机服务健康，最新live auth仍为`InvalidAccessKeyId`；这既不满足H0业务ObjectStore门，也不满足跨故障域生产恢复门。应用identity、对象版本/生命周期、备份和恢复conformance全部通过前，对象相关正式能力保持阻断。
- Explicit non-goals:
  - 不在本 ADR 中选择云厂商、对象产品、WORM 产品、bucket、加密/KMS、备份工具、checkpoint 频率、签名算法或精确保留天数。
  - 不承诺区域级 RPO=0，不把同步副本当作备份，也不把备份存在当作 RTO/RPO 已通过。
  - 不引入 PostgreSQL 与 ObjectStore 的分布式事务；不保存正文副本到 deletion ledger；不把 180 天审计保留期直接当作 deletion-ledger 覆盖期。
  - 不批准业务 Schema、ObjectStore API、删除 UI 或生产部署。

## Rationale and Trade-Offs

- Requirement-linked rationale: 恢复目标约束的是可用的正式业务事实，而不是两个基础设施各自“能恢复”。checkpoint 与独立删除高水位是验证跨存储一致性和防复活所需的最小控制面。
- Trade-offs accepted: 接受consistent-cut控制、分片manifest/Merkle、对账、独立账本、恢复排序和证据保存成本，以换取可验证恢复和删除语义。
- Negative consequences: checkpoint生成可能延迟可恢复点；B1有MVCC快照/物化压力，B2增加每次引用提交的watermark治理；对象清单可能很大；delete intent写入前账本不可用时必须拒绝新删除；intent已耐久但PostgreSQL尚未完成时对象保持不可访问/pending；恢复时cut、分片/Merkle或当前账本高水位不可验证则不能开放；恢复演练更复杂。
- Mitigations: manifest不可变、分页/分片并以Merkle root封顶；B1限制事务/物化窗口，B2用数据库约束和恢复校验守住watermark；账本只保存最小控制元数据；所有状态转换以稳定commandId幂等。ledger已写而PostgreSQL未提交时，reconciliation以delete intent强制不可访问并补齐tombstone；将orphan、缺失引用/分片、pending deletion和高水位滞后纳入告警与周期reconciliation。

## Impact

- Modules, ownership, and dependency direction: 数据/恢复 owner 负责 recovery-set 合同；领域模块只引用 logical object ID，不依赖 MinIO 类型或地址；ObjectStore adapter 与 deletion-ledger adapter 位于组合边界。精确 owner 仍为 TBD。
- Public contracts, data, compatibility, and migration: 需要版本化 checkpoint/manifest、object lifecycle 与删除 receipt 合同。旧数据只有在可生成基线 manifest 且完成校验后才能纳入；破坏性清理需等待兼容窗口与恢复证据。
- Reliability, failure, recovery, and operations: 若 delete intent 尚未耐久而 ledger 不可用，系统拒绝新删除、保持 PostgreSQL/可见状态不变并返回明确失败；若 intent 已耐久但 PostgreSQL 未完成，系统依据 intent 强制不可访问并保持 pending，由 reconciliation 补齐；删除barrier必须收口producer lease/call intent/DeliveryStore写grant并以固定index HWM证明无迟到buffer，已缓冲结果通过 `DISCARDED_BY_DELETION` reconciliation 终结并安全擦除；恢复时 ledger/high-watermark 不可验证，恢复门保持关闭。H0 DataSafety始终要求备份/ledger与待恢复PostgreSQL时间线在逻辑、凭据和恢复控制上隔离并可独立核验；只有`UD-AVL-01`使AvailabilityGate适用时，才额外要求checkpoint、账本和对象备份满足已批准的跨故障域耐久与N-1包络。
- Performance and capacity: checkpoint 清单、hash 校验和删除重放会增加存储与恢复时间；必须用代表性对象数量/大小证明可在确认的 RTO 内完成，不能预填吞吐量。
- Security, privacy, and compliance: 账本仅保存稳定、最小化或假名化标识、命令、时间、序号与校验信息；访问凭据与业务库隔离；备份/对象/manifest 需加密和审计。精确控制待安全与合规 owner 批准。
- Deployment, rollout, rollback/forward recovery: 先以只写不放行方式生成/验证 checkpoint 和 ledger，再进行恢复演练，最后才允许其成为发布恢复门。若方案未被接受或验证失败，生产对象能力保持阻断；已产生的删除记录不能回滚丢弃，只能 forward-reconcile。应用回退不得绕过新格式产生的删除高水位。
- Technical debt introduced or retired: 若接受并实现，可退休“PG 与对象独立最近备份即可恢复”的风险；在 checkpoint 频率、清单规模、ledger 产品和 owner 未冻结前仍保留显式阻断项。

## Implementation and Verification

- File-level plan: 接受后，先分别审批 ObjectStore/Schema/API/删除合同与恢复 runbook；再新增 adapter、manifest/ledger persistence、reconciliation、监控和迁移。当前 ADR 不授权修改这些文件。
- Architecture/contract/failure/performance checks:
  - 合同测试覆盖不可见 quarantine、重复 finalize、重复删除、账本重放、缺失/错误 object version/hash 和恢复开放门。
  - 故障测试分别覆盖 pre-intent ledger outage（拒绝且状态不变）、post-intent/pre-PG 崩溃（不可访问/pending 并对账）、PG 提交前后崩溃、对象成功但 PG 失败、删除barrier与active producer/JIT call/`DELIVERY_BUFFER_CREATE` grant、barrier前call在barrier后返回→仅`DELETION_DISPOSITION` lease/隔离buffer/receipt、伪造或重复处置拒绝、取HWM后旧Worker迟到buffer、`RESULT_BUFFERED`/report/ack各边界交错、index分页gap/重复/不可证、discard receipt 丢失/重复与 secure erase、恢复时 ledger/high-watermark 不可验证、恢复到旧备份、账本重放中断和重复重放。
  - 完整演练必须分别覆盖所选cut算法的并发新增引用、并发删除、checkpoint中断/重试、缺失/乱序分片、Merkle错误、component manifest中schema/config/application-artifact/runbook ref/hash缺失或错配和恢复到旧备份；从独立备份恢复一个application recovery set，并记录timeline/LSN、epoch/watermark、manifest/Merkle、object校验、ledger high-watermark、schema/config/artifact/runbook、唯一约束、RTO与实际数据损失。
  - 用H0及累计版本代表性对象/引用/删除规模测量cut事务、分片构建、checkpoint生成、ledger replay、恢复和验证时间；未有原始结果前状态为Unverified。
- Mixed-version or migration sequence: expand 新生命周期与 manifest 字段；双读/对账旧引用；建立基线 checkpoint；验证旧/新应用兼容；再停止旧写法；最后经单独批准 contract。任一不可逆迁移后使用 forward-fix 或完整恢复，不伪装成简单应用回滚。
- Success and failure evidence: 成功证据包括B1/B2批准记录、不可变分片manifest/Merkle root、PG cut与备份ID、校验报告、ledger cursor/high-watermark、恢复日志、数据对账和有界RTO/RPO结果；任一cut/分片/对象/账本/唯一性校验失败必须记录为Failed/Unverified，不能开放数据或声称通过。当前全部Unverified。

## Revisit Triggers

- Confirmed scale or load threshold: 对象数量/体量、checkpoint 生成时长或 ledger 积压使确认的恢复窗口无法满足；阈值须由代表性测量产生。
- New consumer or implementation: 更换 ObjectStore/备份/ledger 实现，新增金融受许可数据、跨区域恢复或第二个正式二进制数据 owner。
- Reliability/performance budget change: RTO、正式数据 RPO、草稿 RPO、备份窗口、删除期限或故障包络改变。
- Due phase/date: 任何正式 ObjectStore 业务消费和生产预发布之前；未接受及未演练时对应能力保持阻断。
