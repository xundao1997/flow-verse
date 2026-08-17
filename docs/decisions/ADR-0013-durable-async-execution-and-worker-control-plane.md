# ADR-0013: PostgreSQL 耐久作业与 Worker 控制面

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/RELIABILITY_BUDGET.md`；`ADR-0005-operational-diagnostic-chain.md` |
| Supersedes | 仅在接受并实施后 supersede ADR-0005 的 API→Worker 生产诊断方向；当前 N/A |

## Context

- AI、文件处理和导出是长任务；正式状态、费用和结果 lineage 必须耐久且可 fencing。
- 当前 API 主动探测 Worker、Worker 直接探测 PostgreSQL，仅用于诊断；目标业务方向是 Worker→API。
- Redis 已部署但无业务消费者，不应因为存在而成为第二作业事实源。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. PG durable job + Worker pull internal API | 单一 authority、事务一致、当前规模简单 | API/PG 控制面需隔离与容量治理 | Medium | 当前候选 |
| B. Redis durable queue | 快速接入 | authority/持久/淘汰/恢复语义冲突 | Medium | 不满足当前正式性要求 |
| C. 独立 broker + outbox | 高吞吐、解耦 wake-up | 新运维面与最终一致性复杂度 | High | queue/polling 测量达到触发器后 |
| D. API 直接同步调用模型 | 实现少 | 请求超时、恢复和费用未知结果不可控 | Low initially | 仅无副作用短诊断 |

## Decision

- Proposed option A：PostgreSQL 保存 durable job、lease、fencing、result receipt；四类判别式 context 为：AI job 固定`BUSINESS|EVALUATION` purpose与execution/单模型lane attempt/binding/step，文档处理固定object version，导出固定export request，maintenance只允许`DELETION_RECONCILIATION/RECOVERY_CHECKPOINT_BUILD`并固定相应deletion request/recovery checkpoint。Worker以workload identity从private `/internal/v1` claim/heartbeat/report；非AI job不伪造execution lineage，maintenance不开放任意脚本且不成为新data owner。
- Worker 不持有业务 DB repository/credential；业务期 retire/隔离 API→Worker 诊断，避免双向生产依赖。
- Worker 只通过统一 lease/fencing-bound job-input合同获取输入；`GET /inputs`是纯manifest/descriptor查询，所有短时对象与DeliveryStore capability只经幂等`POST /input-grants`签发/续签，`grantRequestId+digest`保证响应丢失不重复分配。typed owner ID不是locator。普通grant绑定job/context/revision/purpose/method/objectVersion/expiry；DeliveryStore写入另用按`job+context+reportKey`唯一的`DELIVERY_BUFFER_CREATE`短时单record/no-overwrite/maxBytes grant并绑定report-envelope ref/hash，同key异hash不得建第二record。删除barrier后普通grant拒绝；只对pre-barrier CALL_START_COMMITTED的同一intent签更高fencing`DELETION_DISPOSITION` lease及业务不可读`DELETION_DISPOSITION_BUFFER`，它不能调用provider、读取原输入或生成第二结果。DELIVERY_RECOVERY只有原buffer/envelope读取权；所有grant禁止bucket list/任意key，过期续签仍重验取消、删除、policy与对象状态。
- claim 使用 long-poll 或有界 exponential backoff+jitter；按 workload class 设公平配额、最大 claim、lease 与饱和拒绝。public/internal 使用独立 semaphore/pool/connection budget。
- 每个AI attempt绑定一个不可变ExecutionBinding且只代表一个model lane；每个AI job固定一个attempt。首次最多三业务模型授权原子创建每lane独立binding/initial attempt/job并共享批次input/slot/总预算上限；retry/fallback只在原lane创建新preview/binding/attempt。provider调用前执行原子JIT call-start：锁job+lease+purpose+evaluation arm+role+lane+step；BUSINESS重验匹配modelProfile activation/最新eligible assessment；EVALUATION重验typed authorization、comparison mode/basis/arm/order、EvaluationBinding/dataset/license/独立预算与`EVALUATION_ARTIFACT_ONLY`，OFFLINE验证管理员authority，SHADOW验证不可变rollout authority manifest与用户D01 consent。provider TARGET只匹配真实PromptConfig arm；typed baseline不是TARGET lane。JUDGE binding只冻结basis-specific dependency selector，所需证据未receipted前不可claim/call-start，实际artifact或baseline refs/hash/receipts只在JIT写入ModelCall resolved-call-input manifest。两者都重验policy/budget/input，落真实调用输入、assessment或authorization ref/hash/kind/basis/arm/role、provider idempotency capability/version、可重建的确定性key derivation或加密key/ref与started marker，再返回短时token和同一exact key。相同intent/hash重领必须得到同一key；不支持受验证幂等时未知调用不得自动恢复。单个EVALUATION结果只形成评测artifact/cost/run progress；只有API finalizer在完整授权plan、validator、hard-fail、basis对应证据集合与所需人审闭合且无stale后才追加一个EligibilityAssessment revision，不能形成business candidate/formal。
- JUDGE依赖集合由basis决定：DIRECT只等candidate TARGET receipt；PROMPT_ONLY等两个provider arm；BASELINE_GATE等candidate receipt与typed HUMAN/NO_AI baseline artifact+人工批准receipt而不创建control ModelCall；FACTORIAL按冻结factor/control plan。JIT和finalizer必须用同一集合，不能把“PAIRED”机械解释成两个provider调用。
- 每个含artifact的Worker result/failure在首次向API report前，都把payload、不含delivery record ref/hash的不可变job-report envelope、单向引用该envelope的delivery record和unreceipted-index entry，在同一跨Worker故障耐久的加密DeliveryStore durability boundary内write-through并取得`RESULT_BUFFERED`，不能因API当前可达而跳过。API先校验envelope hash并预分配稳定record ref，再签单record/no-overwrite grant；record hash冻结envelope ref/hash而envelope不反向引用record，避免自引用。记录按AI/document/export/maintenance封闭context绑定，后续状态只追加。API正常耐久接受同一context/result后返回`ACCEPTED` receipt；若对应task已有耐久deletion intent+tombstone，则不创建用户派生事实，返回`DISCARDED_BY_DELETION`处置receipt。只有两种终态receipt之一经验证后才ack/GC。producer在buffer后首次report前崩溃/lease失效时，API仅可从稳定snapshot/cursor、单调sequence/HWM且无gap的unreceipted index签发`DELIVERY_RECOVERY` lease；恢复者只重报原record/envelope，不调用provider、不改digest或生成新结果。若INT-007或含artifact的INT-008提交后响应丢失，terminal ack可按`job+reportKey`找回已耐久receipt并校验context/delivery/result及producer/acceptance proof，不要求仍持有active lease，且只能ACK/secure erase/GC。index不可证、lag越门或分页gap使对应pool、reconciliation与删除cleanup fail closed；定义容量、retention、满载和 reconciliation。
- 所有buffer写grant在签发capability前先耐久记录`delivery-grant-intent/v1`，冻结预分配record/payload locator、envelope/result hash、purpose和expiry；这组receipt是payload-before-record/index崩溃后的孤儿发现输入。删除交叉若最终无payload，只能由API reconciliation在所有相关WORK/DELETION_DISPOSITION lease和grant失效、逐个已签locator从未可见或已secure erase、固定index HWM完整无record且无竞态后写`NO_PAYLOAD_DISPOSITION_ACCEPTED`并置`OUTCOME_UNKNOWN_NO_PAYLOAD`；proof不表示provider未处理数据，任何边界不可证时cleanup fail closed。
- Redis 只能作为 wake-up 优化；broker 只有 queue age/poll cost/throughput 证据触发，切换仍保持 PG single claim owner、outbox/dedupe。

## Rationale and Trade-Offs

- 以一个关系数据库 authority 降低 MVP 分布式一致性成本。
- 接受 API/PG 控制面压力，使用隔离池、背压、配额和测量缓解；不提前购买 broker 复杂度。
- JIT gate 无法撤销已经越过外部不可逆点的调用，因此明确 in-flight/unknown-outcome，而不伪装取消成功。

## Impact

- Prompt revoke 只阻断尚未通过 call-start 的步骤；已开始步骤保留费用/结果并按政策处理。删除与在途结果相交时仅保留获批的最小非内容费用/审计，payload 经删除处置 receipt 安全擦除。
- Worker crash、lease lost、duplicate report、provider-return/API-outage 必须可交付且不重复正式化；已RESULT_BUFFERED结果通过DELIVERY_RECOVERY恢复交付而不重跑provider，只有受provider合同验证的同一exact幂等键才允许恢复外部调用，否则保持outcome unknown。
- 部署需要 private endpoint、workload identity、DeliveryStore 和 internal readiness，不选择具体厂商。

## Implementation and Verification

- 测试判别式job context：AI的exact purpose/arm/role/lane/attempt/job/step/binding lineage，最多三业务lane原子授权、跨lane binding拒绝、同lane retry/fallback递增、BUSINESS与typed OFFLINE/SHADOW EVALUATION隔离、DIRECT/PAIRED candidate/control与盲化换位、TARGET/JUDGE selector→resolved-input隔离及API finalizer；document的object-version lineage，export的export-request lineage，maintenance的封闭subtype+deletion-request/recovery-checkpoint lineage，以及leasePurpose/expiry/fencing、重复claim/report、empty polling、fairness和pool saturation；未知maintenance subtype/target必须在registration/claim/report均拒绝。四类job input/grant还要覆盖GET无副作用、POST grant同key响应丢失重放/异hash拒绝、过期、同门续签、撤销、删除竞态、`DELIVERY_BUFFER_CREATE`与`DELETION_DISPOSITION_BUFFER`单record/maxBytes/no-overwrite、错误purpose/method/version与list/任意key拒绝。
- crash-point 覆盖 claim 后、call-start 前后、provider 返回后、payload/envelope/index durability boundary各边、首次report前producer崩溃/lease过期后的DELIVERY_RECOVERY、API 持久化前后、INT-007或含artifact INT-008提交后响应丢失+Worker重启的receipt找回、unreceipted-index分页gap/重复/HWM/lag，以及 deletion barrier 停止producer/grant、迟到buffer与 `DISCARDED_BY_DELETION`/secure-erase/reconciliation 路径。
- 代表性负载记录 queue age、claim latency、lock/pool wait、费用和 duplicate suppression；无结果不得启用 Redis/broker。

## Revisit Triggers

- PG/internal API 控制面达到批准的 saturation/queue-age 门；出现多区域 Worker；DeliveryStore 生命周期变化；或第二种独立作业消费者出现。
