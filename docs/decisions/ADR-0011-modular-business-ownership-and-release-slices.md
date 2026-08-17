# ADR-0011: 模块化业务 ownership 与逐版物理切片

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-ARCH-BASELINE / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/ARCHITECTURE_BASELINE.md`；`../engineering/V1_DETAILED_TECHNICAL_DESIGN.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/V1_TECHNICAL_SOLUTION_ADVERSARIAL_REVIEW.md` |
| Supersedes | N/A |

## Context

- 当前 API/Worker 只有非业务边界声明，详细数据册的 103 个逻辑表、107 行Public catalog与10行business internal catalog均未实现。
- V1.0、V1.1、V1.2 是累计产品能力，但每版必须能独立通过自己的交付门。
- 数据 owner 必须唯一，生产依赖有向无环；不能为了未来金融或扩容预建通用工作流、微服务或跨域表。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 一次实现全量逻辑目录 | 文档覆盖看似完整 | 首次迁移/API巨大、验证面爆炸、提前固化未来语义 | High | 范围一次性交付且团队/证据充分时 |
| B. 模块化单体 + 逐版物理 allowlist | owner清楚、事务简单、可累计交付 | 需要严格 traceability 与每版 migration/API 清单 | Medium | 当前候选 |
| C. 直接拆微服务 | 独立部署与扩缩 | 分布式事务、契约和运维成本远超当前证据 | Very high | 独立扩缩、发布、安全 owner 和运维能力都被证明后 |
| D. 延后 owner 决策 | 不提前承诺 | 业务代码继续阻断 | Low now | 合同仍冲突时 |

## Decision

- Proposed option B：保留 Web、API 模块化单体、独立 Worker 三个代码服务。
- 每个业务表、命令、事件和对象元数据只有一个 module/schema owner；跨 owner 只走公开应用接口或同服务显式 application port，不直接导入内部 repository。
- 为 H0/V1.0、H1/V1.1、H2/V1.2 分别生成business物理allowlist，包含到期表、约束、Public/Internal endpoint、internal jobType/family/schema/capability overlay、event、UI route、Prompt family、migration和test；累计逻辑目录不自动进入首个migration/OpenAPI。另生成独立operational allowlist，H0精确保留API `OPS-API-001..003`（`GET /health/live`、`GET /health/ready`、`GET /health/dependencies`）与Worker私网`OPS-WORKER-001..002`（`GET /health/live`、`GET /health/ready`）共5行；它们不计入107行business Public或10行business Internal catalog，且不解锁业务capability。H0 production profile必须成对退役ADR-0005的Web Check页面、public `GET /api/v1/system/chain`和`GET /internal/v1/system/status`，以product/public/internal router、build和依赖负向测试证明无诊断页及API→Worker生产环；三者只可在隔离的non-production diagnostic profile共同保留，批准的5行`OPS-*` health route不随之退役。
- 新模块首次实现时，必须原子更新 Accepted ADR、Architecture Baseline、architecture checker 和 checker self-test；空目录不算实现证据。
- 微服务提取只有在独立扩缩、独立发布、清晰 owner、安全隔离和可运维能力同时成立时重新评审。

## Rationale and Trade-Offs

- 以最小完整垂直切片换取可审计进度，并保留未来提取 seam。
- 接受模块内可以使用具体 ORM/transaction script；没有真实第二实现时不为每张表制造 repository 抽象。
- 代价是维护逐版 allowlist 与跨 owner contract tests；由 release traceability 和架构检查缓解。

## Impact

- API 拥有权威业务状态；Worker 通过 internal API 领取/上报，不持有业务 repository。
- Worker/JIT/DeliveryStore故障按job owner投影：AI到execution、文档处理到P03参考处理、导出生成到D11导出请求。新文档处理和新/重复导出生成fail closed；已生成包只有在ObjectStore当前证明目标version、完整性、授权与可读字节时仍可preview/download，不能用metadata或旧LKG替代。mobile不启动或重试这些处理/生成/恢复命令。
- PostgreSQL 可按 owner 使用逻辑 schema，但 migration 仍保持单 head 与统一发布序列。
- V2 金融只能在独立 PRD/AC/UIUX 后新增隔离 owner，不复用小说表/状态机。
- 回退优先撤销 capability；已落地的新 Schema 使用 forward recovery，不做破坏性降级解释。

## Implementation and Verification

- 为每版生成 requirement/AC → owner → table/API/event/file/test/evidence manifest。
- 检查一表一 owner、无未登记模块、无 API↔Worker 生产依赖环、未到期能力无物理对象；production H0对诊断三件套成对deny且只保留独立operational health allowlist。
- 故障合同测试分别覆盖AI execution、P03文档处理、D11导出请求，证明新处理/生成关闭、正式内容保留、既有包只有在ObjectStore当前可证时可读。
- 只有对应 migration/OpenAPI/contract/integration/E2E 通过后，具体切片才能标实现。

## Revisit Triggers

- 第二个真实消费者证明公共内核语义；某模块需要独立扩缩/发布；团队规模与运维能力改变；或模块边界持续产生跨域事务。
