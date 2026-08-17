# FlowVerse V1 路线与决策治理 PRD 增补（评审稿）

## 1. 文档状态与适用方式

- 状态：`IN_REVIEW`。
- 变更集日期：2026-08-13，Asia/Shanghai。
- 文档补齐复审：2026-08-16；仅同步两层发布门、降级/恢复、H0 性能输入和物理切片等评审合同，不改变 `IN_REVIEW` 状态。
- 变更依据：用户明确要求按 V1.0、V1.1、V1.2、V2.0 路线，同步修订 PRD、UIUX、技术方案和阶段系统决策 Prompt，并在修改后整体 Review。
- 原始证据保持不变：`D:\流域\FlowVerse_V1_需求分析与产品方案_PRD.md`（PRD v1.1）和 `D:\流域\FlowVerse_UIUX_MVP.zip`（UIUX Phase 1）不得覆盖或重新打包。
- 本文是对原 PRD 的版本化增补，不复制整份原文。评审通过后，本文对明确列出的变更点优先；未涉及条款继续以原 PRD v1.1 为准。本文与原 PRD 或 UIUX 出现未登记冲突时，受影响路径停止实施并按 `../governance/EVIDENCE_POLICY.md` 处理。
- 本文不批准 API、Schema、依赖、生产部署或性能结果；这些仍由工程合同、ADR 和验证证据决定。

## 2. 产品路线与累计合同

V1 仍是同一小说任务从创作到真实运营闭环的完整产品合同，但交付拆成三个可独立验收、能力逐步激活的版本。后一版本必须回归前面所有已到期合同。

| 版本 | 目标 | 必需入口 | 最小正式输出 | 本版 Outcome Gate | 本版不包含 |
|---|---|---|---|---|---|
| V1.0 小说创作基础 | 从创意形成可恢复、可 Review、可人工确认和导出的首版小说资产 | P01 → Creation Baseline → P02/P03 | 创作基线、参考使用链、AI/人工候选、Review、作品记忆、正式设定/人物/大纲/首批章节、不可变内容快照 | 首版小说正式快照可重建、可审计、可恢复、可导出；真实投放和 Cycle 不是本版发布依赖 | 实际投放、反馈分析、运营决策和效果比较 |
| V1.1 AI 内容分析与运营复盘 | 将一次真实外部投放及反馈转成有证据的分析和用户正式复盘决定 | 选择 V1.0 正式快照 → Operation Validation Baseline → P04/P05 | 正式包装/发布计划、ActualRelease、一个 Cycle、反馈快照、AnalysisInputManifest、AI 分析候选、正式分析、用户正式决定；继续观察作为独立阶段动作保留 | 至少一个真实有效 Cycle；证据不足时只允许继续观察或有留痕地结束无效，但两者都不满足本版完成门，不能伪造成功 | 紧邻后一有效 Cycle N+1 投放、相邻 Cycle 效果结论 |
| V1.2 AI 创作与运营闭环效果 | 让连续有效对的前一轮正式人类决定真正驱动紧邻后一轮内容/包装变化并再次验证 | 当前有效、可执行下一轮的 `HumanDecision` 与 eligible task/baseline → 在 V1.2 生成并确认下一轮方案 → P03/P04/P05 | Cycle N 决定→方案→执行绑定→候选→新正式版本→Cycle N+1 投放→反馈/分析/决定的完整关系，相邻 Cycle 比较、个人价值判断、后续 Cycle 入口 | 两个编号相邻且真实有效的 Cycle N/N+1；Cycle N 决定实际进入 N+1 输入；效果只表达支持程度、干扰和未知，不宣称因果或市场验证。正常路径可以是 1→2，但无效 Cycle 编号不重排 | 自动发布、自动决策、增长/收益保证 |
| V2.0 金融研究 | 股票、基金、期货的有来源、有时点、可复现研究与复盘 | 独立金融 Research Intake | 独立金融 PRD/AC/UIUX 批准后定义 | 股票→基金→期货分别通过数据许可、领域语义、point-in-time、人工确认、合规、HA/性能门 | V1 预建金融表/路由、自动交易、券商连接、个性化投顾 |

版本能力必须由服务端 capability 决定。未进入当前版本的 route/action 不能只靠前端隐藏：新建对象返回不可用原因；历史对象若存在则按批准的兼容策略只读；未知深链安全失败，不创建半成品业务状态。

### 2.1 V1.0 数据安全门与可用性门（`IN_REVIEW / Proposed`）

V1.0 的产品完成与生产可用性声明使用两个独立门，不允许把未批准的生产拓扑反向变成小说创作能力的默认前置条件：

- `DataSafetyGate` 是 H0 强制门。它要求 PostgreSQL 权威记录、对象资料/导出物及其引用关系处于一致的可恢复集合；正式写、幂等、备份/PITR、恢复演练、删除后不复活、历史可读和失败时的保守降级均有可核验证据。Redis 只能是非权威加速或协调能力，丢失它不得改变正式事实。
- `AvailabilityGate` 是独立的部署/运营门，只有在目标环境、测量窗口、故障域、预算、监控与责任人获得另行人工批准后才成为对应发布或对外可用性声明的前置条件。当前唯一 Confirmed 的可用性数值是内部 MVP 验证期 `99%`，不是商业 SLA。
- `99.9%`、多可用区、仲裁/防脑裂、N-1 容量和相应副本数仍是 `Proposed`。未另行批准时，它们不能导致 H0 产品能力被判失败，也不能被用于宣称已经达到高可用；若批准为 V1.0 生产服务等级，则必须在发布前单独取证。
- 未启用 `AvailabilityGate` 不能豁免 `DataSafetyGate`。反之，通过数据恢复证据也不能替代可用性测量或支持 `99.9%` 声明。

## 3. Stage 0 拆分

原 PRD 的 Stage 0 用户旅程保留，但其正式基线拆成两个不可变版本对象，避免 V1.0 被尚未启用的运营信息阻断。

服务端和 UI 分别使用 `creationReady`（仅需 CreationBaseline，可进入 V1.0 创作）与 `operationReady`（两部分均确认，可进入 V1.1 投放/Cycle）语义；禁止用一个未限定的“Stage 0 已完成”布尔值同时驱动两版 capability。

### 3.1 Creation Baseline（V1.0 必需）

唯一字段分配如下；其他文档和 UI 只可引用或逐字段保持一致，不得另建一套 Stage 0 字段：

- 任务名称；
- 创作起点/创意，以及可选的必须保留、必须避免、已有元素；
- 题材、目标读者和任务/创作目标；
- 初始大纲/首批章节范围和语言强度；
- Review 配置；
- 允许的模型池、候选数量默认值和适用的创作预算；
- 参考权利声明与允许使用的内容边界（无参考时明确为不适用）；
- 首批创作范围及其业务完成口径（例如到哪一版大纲/哪些首批章节），不得向用户暴露内部 release 状态作为基线字段。

确认后创建 `CreationBaselineVersion`。修改产生新版本；已经形成的正式内容、执行和快照继续绑定原版本，不追溯改写。

`CreationBaseline` 是初始创作批次的正式约束与初值 owner：它冻结允许模型池、语言约束、适用预算边界和初始候选数默认值。高级设置只拥有后续执行的偏好版本，不能扩大基线允许范围；每次 D01/`ExecutionBinding` 必须记录本次实际模型、参数、候选数、语言与预算。改变正式约束必须创建替代 `CreationBaselineVersion` 并传播影响，只在既有边界内改变未来偏好才更新高级设置。基线中的参考权利边界也不能替代每份资料自己的来源、权利和本次实际使用记录。

### 3.2 Operation Validation Baseline（进入 V1.1 前必需）

唯一字段分配如下：

- 单一目标平台与账号标识；
- 正式内容/包装的投放范围；
- 指标定义、单位、累计/区间口径和时区；
- 正式观察点和数据完整性要求；
- Cycle 预算；单任务业务 AI 总预算和每次执行上限仍由任务级预算政策管理并在此引用，不重复成为一套可漂移的基线字段；
- 连续两个有效 Cycle 的验证目标、比较限制和不可宣称项；
- 人工主动协调时间基线，或明确记录“无可靠基线”。

确认后创建 `OperationValidationBaselineVersion`。从连续验证候选对的前一有效 Cycle 创建起，至紧邻后一有效 Cycle 的正式决定完成，影响可比性的字段保持冻结；必要修改创建新版本、保留历史绑定，并按影响重新计算连续验证起点。无效 Cycle 编号不重排，因此不得把冻结终点硬编码为 Cycle 2。

## 4. AI、系统与人类的决策权

所有阶段使用统一的 D/S/H 责任模型：

| 层 | 可以做 | 不可以做 | 输出 |
|---|---|---|---|
| D：确定性系统 | 身份、权限、对象归属、revision、状态机、预算、时点、唯一约束、版本新旧、数据许可、引用存在、确定性计算、capability | 文学偏好、模糊语义解释 | 权威只读状态、合法动作集合、确定性硬门；正式写入仍需命令 |
| S：语义模型 | 意图/字段/风险/差异/问题/证据/反证/行动候选的封闭分类 | 权限、正式状态、Cycle 有效性、最终合规裁定、风险接受、人类决定或任何副作用 | 不可信但可校验的 `SemanticFindingCandidate` |
| H：人类 | 审阅/更正事实、选择候选、确认正式内容/投放/反馈/分析、作出正式决定 | 绕过最终合规阻断、改写历史、违反 capability | 用户明确提交后，由 D 层重验并形成正式记录 |

固定流程：

`权威状态 → D 前置门 → 必要时调用 S → Schema/枚举/引用后验校验 → 页面展示候选 → 用户明确选择/提交 → D 重新校验 → 正式命令`。

S 层不得直接触发 mutation，不得把推荐动作直接变成页面正式主 CTA，也不得返回可信的 Prompt/Bundle/input hash 元数据；这些元数据由执行器在模型输出外包装。

## 5. 合规决策

原 PRD 的“用户和管理员均不能绕过最终合规阻断”继续有效，但需要区分语义候选和权威裁定：

1. 确定性规则命中可以直接形成权威 `ComplianceDecision=BLOCK`。
2. 语义模型只输出 `NO_RISK_FOUND / RISK_FOUND / INSUFFICIENT_EVIDENCE / NEEDS_HUMAN_REVIEW` 及证据位置、风险类型和建议处置，不能自行形成最终 PASS/BLOCK。
3. 高风险语义命中进入 `PROVISIONAL_HOLD`；在当前没有独立合规复核人的 V1，解除方式默认是修改内容/权利范围后重新检查，不允许管理员强制通过。
4. 若未来引入合格复核人，复核结论形成版本化 `ComplianceDecision` 并保留候选、证据、复核人、时间和规则版本；仍不允许业务用户或普通管理员绕过最终 BLOCK。
5. 检查服务不可用或证据不足时 fail closed：可以保存草稿/候选和人工事实，但不能正式确认、投放或进入模型优化。

## 6. Prompt 生产治理与效果保证

Prompt 不是单一文本文件，也不能用一次演示证明有效。治理对象拆成：

- `PromptConfigBundle`：Prompt 正文、family/version、精确模型/参数、renderer/context builder、输入变量 Schema、输出 Schema、工具/动作白名单、Review/政策版本；它是可评测和可激活的稳定配置。
- `EvaluationBinding`：PromptConfigBundle + Golden Set/rubric/judge/human labels + 评测结果；它证明的是冻结配置在已声明分布上的表现。
- `ExecutionBinding`：已激活 PromptConfigBundle + 本次输入/参考 manifest、实际价格/服务商政策和 hash；它是一次执行的不可变追溯记录，不因普通输入变化重新走全量 Prompt 晋升。

Prompt 状态：

`Draft → Candidate → OfflinePassed → HumanApproved → ExplicitPilot/Shadow → ControlledCanary → Active → Deprecated/Revoked/RolledBack`。

- 自动评测最多推进到 `OfflinePassed`。
- 首个版本没有 last-known-good 时，走 `HumanApproved → ExplicitPilot → ControlledCanary → Active`；任一停止条件触发即禁用对应 AI 能力并回到人工/确定性流程，不能跳过受控 Canary。
- 第二版开始才能以 last-known-good 作为回退目标。
- Prompt 作者不能独自批准自己的版本。V1 默认由业务用户/领域评审确认效果、管理员执行激活；高风险合规 Prompt 还需要独立合规责任人。若角色未就绪，该 family 不得 Active。
- 客观规则用确定性检查或基于证据的 direct evaluation；主观质量用盲化 pairwise，A/B 换位两次，不一致即 TIE/低置信度并转人工。
- LLM judge 只辅助筛选，不作正式事实、合规裁定或上线批准。
- 评测门按风险分级：router/extractor 使用 Schema、非法动作率和人标分类；分析/决策增加引用支持、证据不足降级和领域人评；合规/金融增加隐藏集、阻断漏检、独立复核和严格试运行。

系统决策 Prompt 的完整合同见 `../ai/SYSTEM_DECISION_PROMPTS.md`。

## 7. V1.1 运营事实与分析

### 7.1 外部事件

外部事件至少支持：

- `REJECTED`
- `RELEASE_FAILED`
- `EXTERNAL_INVALID`
- `PLATFORM_REMOVED`
- `EXTERNAL_DELETED`
- `MINOR_EDIT`
- `MATERIAL_CONTENT_EDIT`
- `MATERIAL_PACKAGE_EDIT`
- `AI_LABEL_CHANGE`
- `PLAN_MISMATCH`

模型只能建议分类；事件事实由用户确认，Cycle 影响由 D 层按事件时间、正式观察点、版本和当前状态确定。

### 7.2 敏感反馈

反馈保存与模型使用分开。模型只产生 `NO_RISK_FOUND / POTENTIAL_PII / POTENTIAL_SENSITIVE / POTENTIAL_PROHIBITED_SECRET / NEEDS_HUMAN_REVIEW` finding；D 层独立形成：

- `modelUseStatus=NOT_REQUESTED`
- `modelUseStatus=READY`
- `modelUseStatus=NEEDS_REDACTION`
- `modelUseStatus=EXCLUDED_BY_USER`
- `modelUseStatus=BLOCKED_BY_POLICY`

粗俗、负面或拼音谐音评论不因表达方式自动禁止保存；用户可以去标识后作为外部事实确认。截图只供人工查看，不 OCR、不进入 Prompt。凭证、密钥等禁止型秘密不得保存进普通反馈正文。

### 7.3 AnalysisInputManifest

每个分析候选和正式分析必须绑定不可变输入清单，至少包含：

- task、Cycle、ActualRelease 与外部实际版本引用；
- 内容快照、包装版本、章节范围；
- OperationValidationBaselineVersion、指标定义和正式观察窗；
- 外部事件及干扰；
- 被采用的精确反馈快照集合；
- PromptConfigBundle、ExecutionBinding、模型和规则版本；
- 输入 hash、生成时间和 stale 状态。

任一权威输入更正后，旧分析保留但标记 stale/invalidated；新正式分析只能基于新的 manifest 产生。

### 7.4 继续观察

`CONTINUE_OBSERVING` 是独立 Cycle 阶段动作，不是 `HumanDecision`：

- 不关闭 Cycle；
- 用户确认新观察点和理由；
- 当前正式分析标记为待新证据复核；
- 驾驶舱下一步转为等待/回填新观察点。

只有用户从 `ENTER_HUMAN_DECISION` 进入正式决定流程并确认决定，才可以在有效条件满足时正常关闭 Cycle。

## 8. V1.2 下一轮与效果

下一轮方案候选和用户确认字段至少包含：目标、具体改变范围、参考、Agent、模型、候选数量、预算、预期变化和下一次发布计划。模型建议不能跳过 Review、作品记忆、合规或人工正式确认。

相邻 Cycle 的可比等级由 D 层从平台、账号、指标定义、单位、口径、实际观察时长、版本链和重大事件权威计算；语义模型只能补充反证、干扰和未知，不返回或升级可比等级。语义叙述超出 D 层边界时，候选失效并按当前权威输入重做。

个人价值由确定性公式计算：

- 主动协调时间相对可靠基线下降至少 30%；
- “阶段清楚、下一步清楚、Review/分析帮助决策”三项均值至少 4/5；
- 用户愿意或已开始首个连续有效对之后的下一 Cycle N+2（正常 1→2 路径下即 Cycle 3）；
- 严重信任事故为否决项。

有可靠时间基线时，前三项满足至少两项且无严重事故为通过；只满足一项为不确定；均不满足或用户因产品本身放弃为未通过。没有可靠时间基线时，评分与后续 Cycle N+2 意愿必须同时满足，否则为不确定/未通过。结果始终分开显示功能闭环、机制、个人价值、外部证据充分度和“市场未验证”。

## 9. Agent/模型累计验收

不得为了验收形式化启动无关 Agent。角色和模型按版本累计：

| 版本 | 到期角色证据 | 模型证据 |
|---|---|---|
| V1.0 | 主编/协调、章节创作、编辑评审真实参与；其他创作角色按任务需要 | 至少两个获准模型针对同一创作简报独立候选；实际版本和选择理由可追溯 |
| V1.1 | 在 V1.0 基础上，运营分析真实参与 | 三个批准 provider family 到本版结束前均至少在获准真实范围参与一次；不适用/黄色范围不得为凑数启用 |
| V1.2 | 改文导演真实参与，上一轮决定进入新执行清单 | 至少一次模型差异影响人类选择；完整 V1.0～V1.2 执行链可审计 |

若某 provider 因政策、可用性或数据范围不能合法参与，相应累计里程碑保持未完成或由后续批准的替代 AC 修订处理，不能静默换模或用合成调用充数。

## 10. UIUX 与设备

- D 层解析出的唯一主动作仍是页面唯一正式主 CTA。
- S 层行动候选以“建议/候选”展示；多个合法低风险动作并存时，唯一主 CTA 是“审阅并选择下一步”，而不是模型直接指定的 mutation。
- 每个 owning page 使用同一 Decision Candidate 语义组件展示证据、反证、未知、证据不足、过期和人工复核；不新增全局 Prompt 工作台。
- 390×844 保持业务只读；D10 的 pause/resume/terminate/archive/delete 均禁用。D11 已生成包的预览/下载和 D12 简单问卷是明确例外，不能借此开放其他正式动作。
- 768～1279 默认视为 compact desktop：保留正式状态和唯一主动作，次要上下文改覆盖层；若实际宽度/输入能力不能安全承载正式操作，显示明确的不支持原因并要求使用至少 1280×720 的批准桌面环境。

## 11. 分版本验收和证据

每条需求/AC/UIUX 场景都必须登记：`introducedIn`、`requiredFrom`、适用版本、N/A 理由、模块/数据 owner、D/S/H 或 Prompt family、测试、证据和发布门。

### 11.1 物理 capability allowlist

下表是 `../uiux/RELEASE_CAPABILITY_MATRIX.md` 的产品级摘要；route、dialog、viewport 和子场景仍以该矩阵逐项登记，不能仅凭页面壳存在推断某项能力已进入当前版本。

| Gate | 本版物理 allowlist | 明确尚未引入 |
|---|---|---|
| H0 / V1.0 | AUTH、P01、Stage 0 的 `CreationBaseline`、P02、P03 初始创作；当前版本范围的 Bot/Agent trace/待处理/设置/活动；A01–A08 的 V1.0 范围（含 A05）；D01、D02 内容确认、D03、D10、D11 内容包 | P04、P05、V1.1 运营字段与工作负载、D02 包装模式、D04–D09、D12、下一轮/比较/价值能力 |
| H1 / V1.1 | H0 全量 + Stage 0 的 `OperationValidationBaseline`、P03 包装交接、P04、P05 分析/决定；A01–A08 的 V1.1 扩展；D02 包装模式、D04–D09、D11 运营复盘包、D12 `cycleTimeReconciliation` | P05 下一轮/相邻 Cycle 比较/个人价值、V1.2 决策驱动创作、D12 `twoCycleSurvey` |
| H2 / V1.2 | H0/H1 全量 + P03 决策驱动创作、P05 下一轮/比较/价值/后续 Cycle N+2；A01–A08 的 V1.2 扩展；D11 完整链路包、D12 `twoCycleSurvey` | V2 金融 route、对象、数据与动作 |

历史正式对象在后续版本继续可读；不在 allowlist 的新建、mutation、Bot 动作、待处理项和深链必须返回“当前版本未启用”并安全失败，不能创建半成品状态。

### 11.2 横切门与完成证据

| Gate | 必需横切门 | 最小完成证据 |
|---|---|---|
| H0 / V1.0 | 所有 V1.0 首次到期 AC/UIUX/Prompt；身份与权限、候选/正式分离、人工确认、合规、桌面/compact/mobile fail-closed、`DataSafetyGate`、导出/删除/恢复、安全、可访问性和 H0 性能基准。`AvailabilityGate` 仅在另行批准适用时加入 | 物理 allowlist/拒绝清单；逐子断言和逐场景 evidence ref；首个正式小说快照的重建、审计、恢复、比较与内容导出证据；备份/恢复/删除不复活演练；H0 基准报告及所有待决参数；未引入 route/action 的负向证据 |
| H1 / V1.1 | H0 全量回归 + V1.1 首次到期门 + 新增 provider/Prompt/对象/降级/性能范围重新取证 | H0 历史保持证据；一个真实有效 Cycle 的 ActualRelease→反馈→正式分析→正式人类决定链；`continue observing` 与无效 Cycle 的负向证据；V1.1 allowlist 与拒绝清单 |
| H2 / V1.2 | H0/H1 全量回归 + V1.2 首次到期门 + 完整横切范围重新取证 | 首个相邻有效 Cycle N/N+1 的决定→方案→执行→正式变化→投放→复盘链；比较等级、个人价值、后续 Cycle N+2 路径；PRD 7.5/7.6、AC-01～35 与 UIUX 1～130 的逐项 evidence ref |
| V2 | 独立金融 H2.x | 独立 PRD/AC/UIUX、数据许可、point-in-time、合规、HA/性能和真实研究证据；小说证据不可替代 |

### 11.3 H0 基准输入与待批准参数

外部 PRD 已确认的容量边界必须直接进入 H0 数据夹具：单任务最多 `20` 个文件、单文件最多 `10 MB`、单文件最多 `50 万字符`、单任务合计最多 `200 万字符`、文字 PDF 最多 `300 页`；小说默认起点为 `20 章大纲 + 首批 3 章`，但用户可在 Creation Baseline 中调整。前五项是上限夹具，默认创作范围是代表性起点，两者不能混写成同一硬编码业务限制。

这些数值只是已确认的测试输入，不是性能已达标证据。H0 基准的目标环境/资源、网络、冷/热缓存、并发与队列、样本量/测量噪声，以及把既有产品响应目标落到每条测试的警告/失败阈值仍待人工批准；在此之前性能状态保持 `Unverified`。

### 11.4 发布前用户决策点

| Decision point | 用户需要确认的最小内容 | 未确认时的处理 |
|---|---|---|
| `UD-PG-01` PostgreSQL | V1.0 权威 writer/故障域、备份/PITR、正式记录 RPO 的实现边界及运维 owner | `DataSafetyGate` 保持阻断；不得以当前健康检查替代正式数据恢复证据 |
| `UD-OBJ-01` 对象存储 | 业务账号/bucket、TLS/加密、隔离、生命周期、版本/删除、备份恢复及与 PostgreSQL 的一致恢复点 | 引用上传、对象依赖正式写、导出和恢复路径保持不可发布；不得把中间件进程健康视为业务对象合同 |
| `UD-REC-01` 恢复 | 数据集清单、RTO/RPO 测试范围、恢复 owner、删除账本/等价机制及“恢复后不复活”核验 | H0 `DataSafetyGate` 保持 `Unverified` |
| `UD-DEG-01` 降级 | PostgreSQL、对象存储、AI/provider、队列/过载分别允许的只读、草稿保留、正式写阻断、重试与用户说明边界 | 受影响正式写和 AI 执行 fail closed；不得静默展示未知新鲜度数据或无限重试 |
| `UD-PERF-01` 性能 | H0 基准环境、并发、样本、命令、噪声和逐项阈值；已确认容量输入不得删减 | 性能发布门保持 `Unverified`，且不能据此提前引入缓存、读副本或新队列 |
| `UD-AVL-01` 可用性 | 是否仅按 Confirmed 的内部 MVP `99%` 验证，或另行批准生产 `AvailabilityGate`；若批准，还需故障域、窗口、预算、告警和责任人 | 不得宣称 `99.9%` 或生产 HA；`DataSafetyGate` 仍照常执行 |

55 个 UIUX exact 场景可作视觉基准；75 个 representative 只证明复用模板关联，仍需行为断言。原 UIUX 自验证报告的 `passed` 与 `missing/not found` 冲突继续为 Unverified，不得作为实现通过证据。

## 12. 明确未批准事项

- 本增补不批准完整既有连载导入或独立外部内容 AnalysisSession。
- 不批准用户侧 Prompt 查看/编辑、自由 Prompt 工具箱、自由 Agent、通用 Workflow Builder 或 Prompt 市场。
- 不批准 V2 金融表、API、行情源、组合/回测、TimescaleDB hypertable、pgvector 索引或交易能力；组合和回测是否进入 V2 必须等待独立 PRD。
- 不因文档完成宣称任何 Prompt、HA、性能、安全、恢复或 UIUX 已实现或通过。

## 13. 本增补批准门

整体 Review 必须确认：

1. 本文与 `V1_PRODUCT_BRIEF.md`、`../uiux/`、`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md`、`../ai/SYSTEM_DECISION_PROMPTS.md` 和 `../tasks/V1_IMPLEMENTATION_PLAN.md` 术语一致。
2. 所有 P0 冲突已删除或显式保留为阻断性待决策，不能同时存在两个可实施答案。
3. 所有新增枚举有 owner、状态影响、失败路径和人工责任。
4. Prompt 评测只证明冻结配置在声明范围内的表现，不把 LLM judge、单用户偏好或自然 Cycle 变化解释成客观效果或因果。
5. 原始外部 PRD/UIUX 包、hash、批准历史和未受影响合同保持可追溯。
