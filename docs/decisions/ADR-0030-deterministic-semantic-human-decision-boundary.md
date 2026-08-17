# ADR-0030: 确定性系统、语义模型与人类确认的决策边界

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-13 |
| Scope IDs | FV1-ROADMAP-REVIEW |
| Evidence | `../intake/V1_PACKAGE_INTAKE.md` 中 `FV1-ROADMAP-REVIEW=IN_REVIEW`；`../ai/SYSTEM_DECISION_PROMPTS.md` 2～3、6～10、13；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` 9.12、TD-29；`../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md` 4、6～8；`../uiux/ACCEPTANCE_CRITERIA.md` |
| Supersedes | N/A |

Allowed status values: Proposed, Accepted, Rejected, Deprecated, Superseded.

本 ADR 只是候选权责合同。它不接受任何 Prompt family、API、Schema、UIUX 或业务状态机，也不证明模型判断正确。

## Context

- Problem: 系统阶段既有确定性的权限/版本/状态/预算/时间/许可规则，也有意图、风险、差异、证据解释等模糊语义。若让 LLM 直接输出最终 PASS/BLOCK 或 mutation，它会成为不可重放的权限/状态机；若完全不用模型，复杂语义 Review 的人工负担又过高。当前 UIUX 还必须明确承载候选到正式命令之间的用户动作。
- Confirmed requirements: AI 输出永远是候选；人类确认每个正式事实；管理员不能代替用户确认；正式/高风险命令必须服务端重算 capability、校验 revision/idempotency 并返回权威 receipt；Bot 失败不能阻断确定性入口。
- Constraints: 具体 family、枚举、JSON Schema、阈值、UI 组件和模型均未批准；模型输出可能幻觉 ID、越权引用、未知枚举或不一致证据；系统不得请求/保存隐藏推理过程。
- Current module/contract/data/reliability facts: IN_REVIEW 文档已提出 D/S/H 分层、`SemanticFindingCandidate`、evidence locator、abstention、人工升级和 D2 重验；UI 组件名称为 `DecisionCandidatePanel`，尚无实现或模型评测证据。
- Why a decision is required now: V1.0 Review/合规、V1.1 分析/复盘、V1.2 下一轮方案，以及未来金融研究都依赖同一安全决策骨架。前后端与 Prompt 必须使用同一权责语义。

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| A. LLM 直接决定 PASS/BLOCK/下一动作并执行 | 自动化高、交互短 | 幻觉/提示注入可改变状态；不可证明权限、版本和一致性；高风险 | Medium | High | 不适用于正式事实与当前人审要求 |
| B. 全部使用确定性规则 | 可重放、易审计 | 无法充分处理开放语义；规则膨胀、人工负担高 | Medium/High | Medium | 语义空间封闭且规则可完整定义时 |
| C. D1 前置门 → S 语义候选 → 后验校验 → UI 显式审阅 → H 提交 → D2 重验 | 结合确定性安全和语义辅助；可降级、可审计 | 多一步交互；需 typed contracts、证据定位和冲突处理 | Medium/High | Low | 当前推荐候选 |
| D. 暂停语义自动化，人工 Review | 安全边界清晰 | 成本和时延高，AI 价值下降 | Low | None | family 未批准、不可用或风险过高时 |

## Decision

- Chosen option: **Proposed Option C，并以 Option D 作为安全降级**。
- Scope:
  - D1（Deterministic pre-gate）先基于权威状态计算 actor/role、task/object 归属、current revision、状态机、预算/配额、时点、政策/数据许可、引用存在性、允许 labels/actions 和 hard gates。唯一确定答案直接返回权威只读状态；非法请求不调用模型。
  - S（Semantic LLM）只在批准的窄 family 内回答单一 decision question，并只返回 typed `SemanticFindingCandidate`：封闭枚举、输入内 evidence locator、不确定性/abstention、简短 rationale 和候选动作。它不拥有正式事实、状态、费用、Cycle 有效性、合规最终裁定或副作用；模型自报置信度默认不进入用户合同。
  - 模型不能返回最终 `PASS/BLOCK`。合规 family 只能返回 `NO_RISK_FOUND / RISK_FOUND / INSUFFICIENT_EVIDENCE / NEEDS_HUMAN_REVIEW` 等语义 finding；最终 `ComplianceDecision=PASS/HUMAN_REVIEW/BLOCK` 由 D 层结合确定性规则、validated finding 与必要人审形成。
  - executor 对 S 输出执行完整 Schema、枚举、ID、版本、引用、policy 和 allowed-set 后验校验。不存在、越权、stale、未知枚举、引用超出 input manifest 或 Schema 失败使整份候选无效并 fail closed；不从自由文本“修复”成合法命令。
  - 有效候选只在所属业务主页面的 `DecisionCandidatePanel` 候选 UI 中展示证据、不确定性和“需人工复核”。用户必须明确选择/编辑并提交；模型推荐不能自动成为 primary CTA 或 mutation。管理员不得代用户确认业务事实。
  - D2 在提交时重新读取权威状态，重验 actor、revision、状态/transition、capability、预算/政策、引用、idempotency、候选是否 stale，并用事务写正式事实与 receipt。D1 结果不作为 D2 的缓存授权。
  - router/triage/reviewer/evaluator/action-advisor family 分离；每个 family 只有一个窄问题、封闭 taxonomy、允许输入与输出、升级路径和无 AI fallback。双模型分歧不多数投票自动裁决，按风险矩阵升级人工或取更保守候选。
- Explicit non-goals:
  - 不让 LLM 充当 RBAC、状态机、计费器、时钟、数据许可引擎、最终合规门或正式命令执行器。
  - 不允许链式候选自动互相触发、通用 Agent/DAG、自由 Prompt/工具接线或模型生成新枚举/ID。
  - 不请求、保存或展示隐藏 chain-of-thought；只保存短 rationale、结构化 finding 和输入内证据锚点。
  - 不在本 ADR 批准精确 family 文本、Schema、阈值、UI copy、业务命令、API 或模型。

## Rationale and Trade-Offs

- Requirement-linked rationale: D 层适合稳定、可证明的规则，S 层只补充语义候选，H 层承担正式业务判断；D2 消除候选生成到提交之间的 TOCTOU/stale 风险。
- Trade-offs accepted: 接受显式 Review 和二次验证带来的交互/延迟，以守住人类控制、权限、版本和审计边界。
- Negative consequences: 用户可能感觉步骤变多；候选经常 abstain 或升级人工；D/S taxonomy 和 UI 必须同步维护；模型不可用时自动化价值下降。
- Mitigations: 每页一个基于 D 层的明确 primary CTA；候选面板只在有价值时出现；允许批量人工 Review 但不跳过逐对象证据；按 family 测量保留/修改/驳回和人工负担。

## Impact

- Modules, ownership, and dependency direction: API/领域服务拥有 D1/D2 与正式事务；Worker/Prompt runtime 只生成候选；Web 展示权威 capability 和候选并收集明确 H 命令。依赖保持 Web → API、Worker → API；模型不能直写领域表。
- Public contracts, data, compatibility, and migration: 需要 versioned D1 context、allowed sets、candidate schema、evidence locator、candidate status/staleness 和正式 receipt。新增 enum additive；未知 enum fail closed；历史候选不追溯变成正式事实。
- Reliability, failure, recovery, and operations: 模型/provider/registry 故障时保存原输入并转人工/确定性路径；Bot 区域降级不影响工作主页入口。候选丢失不得损坏正式状态；正式 receipt/idempotency 位于权威存储。
- Performance and capacity: D1/D2 增加两次权威读取与校验；S 为有界异步工作，不能阻塞普通确定性页面。需分别测候选生成、人工 Review 主动时间和正式命令延迟。
- Security, privacy, and compliance: 只传最小授权 input manifest；allowed IDs/actions 由服务端提供；输出引用逐项校验；截图、secret、其他任务和未授权数据不入模；Prompt injection 不能扩大工具或权限。
- Deployment, rollout, rollback/forward recovery: 新 family 先 shadow/人工对照，再启用只读候选，最后才允许候选进入显式提交 UI；任何严重错误立即撤销 family，保留 D+H/no-AI 路径。回退不删除历史候选或正式 receipt，也不自动逆转用户已确认事实。
- Technical debt introduced or retired: 退休 LLM 最终 PASS/BLOCK、自动 mutation 和候选直连下一步的风险；引入 taxonomy、candidate UI 和 D1/D2 合同维护成本。

## Implementation and Verification

- File-level plan: 接受后，按版本先冻结 family registry、D/S/H mapping、candidate/UI/command 合同和 owner，再实施 API/Worker/Web。当前 ADR 不授权业务代码或 Prompt 激活。
- Architecture/contract/failure/performance checks:
  - 权限、归属、revision、状态、预算、政策、允许枚举/动作和 idempotency 的 D1/D2 单元/契约测试。
  - adversarial 输出：虚构/越权 ID、未知 enum、stale revision、manifest 外引用、Schema 破坏、提示注入和模型自报 trusted metadata 全部 fail closed。
  - E2E 证明候选只读展示、证据可定位、用户有显式提交、管理员不能代确认、提交时 D2 冲突不会写副作用。
  - 故障/性能验证 provider timeout、registry/hash mismatch、双模型分歧、abstention、manual fallback，以及确定性入口在 AI 故障下的预算。
- Mixed-version or migration sequence: 先部署能忽略未知候选类型的 reader 和 D2 gate，再生成 shadow candidate，随后启用 UI，最后按 family activation。旧客户端不得通过缺少候选 UI 的命令绕过人审；不兼容时 capability 关闭。
- Success and failure evidence: 需要 contract/E2E/adversarial 测试、candidate→UI→H→D2 receipt trace、人工判例、模型评测和故障降级原始结果。只存在 Prompt 文档或模型返回合法 JSON 不是 Passed。

## Revisit Triggers

- Confirmed scale or load threshold: 人工升级率、修改/驳回率、Review 时间、模型延迟/成本或 D1/D2 负载超过获批预算。
- New consumer or implementation: 新高风险命令、工具调用、多 Agent、自动外部发布、金融研究/分享或第二个业务领域使用同一 family。
- Reliability/performance budget change: 正式命令延迟、AI 等待、人工 Review、错误预算或安全零容忍项变化。
- Due phase/date: 首个 decision family 激活和每个版本 Scope/Contract Gate 前；未接受或 family/UI/D2 未一致时仅允许确定性/人工路径。
