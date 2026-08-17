# FlowVerse 文档入口

本目录集中保存 FlowVerse 的产品、UIUX、详细技术设计和系统决策 Prompt 文档。仓库内文档是面向评审、实施与验收的可追踪文档集；原始 PRD v1.1 和 Phase 1 UIUX 包的文件身份、哈希与批准范围只以 [V1 Package Intake](intake/V1_PACKAGE_INTAKE.md) 为准，不在仓库中复制第二份权威原件。

## 状态与权威边界

- 原始产品与设计基线：PRD v1.1 + Phase 1 UIUX MVP 包，状态和证据见 [V1 Package Intake](intake/V1_PACKAGE_INTAKE.md)。
- 本轮仓库补充文档：除各文件另有明确声明外，均为 `IN_REVIEW / Proposed`；它们不代表 API、Schema、依赖、ADR、部署、Prompt 激活、UIUX、HA、恢复或性能已经批准或实现。
- 冲突处理：按 [Evidence Policy](governance/EVIDENCE_POLICY.md) 停止受影响路径并登记裁决，不得静默选择其中一份。
- 当前实现状态：以 [Technology Stack Registry](engineering/TECH_STACK.md) 和 [Architecture Baseline](engineering/ARCHITECTURE_BASELINE.md) 为准，不得从设计文档反推“已经实现”。

## PRD 与产品路线

- [Product Positioning](product/PRODUCT_POSITIONING.md)：产品定位、长期边界和 V1/V2 方向。
- [V1 Product Brief](product/V1_PRODUCT_BRIEF.md)：V1 产品目标、累计版本、基线与完成条件摘要。
- [V1 路线与决策治理 PRD 增补](product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md)：V1.0 小说场景、V1.1 内容分析与运营复盘、V1.2 创作与运营闭环，以及 V2.0 金融研究方向的版本化增补。
- [Acceptance Criteria](uiux/ACCEPTANCE_CRITERIA.md)：产品、UIUX、降级与逐版本验收合同。
- [V1 Implementation Plan](tasks/V1_IMPLEMENTATION_PLAN.md)：按版本和横切门组织的实施顺序、停止条件与证据要求。

## UIUX

- [UIUX Principles](uiux/UIUX_PRINCIPLES.md)：体验原则、桌面优先、移动只读和单一主动作。
- [Release Capability Matrix](uiux/RELEASE_CAPABILITY_MATRIX.md)：V1.0/V1.1/V1.2 页面、动作、场景和能力首次到期矩阵。
- [Interaction Rules](uiux/INTERACTION_RULES.md)：页面、状态、候选/正式对象和人工确认交互规则。
- [System Degradation and Recovery UIUX](uiux/SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md)：降级、新鲜度、重试、结果未知和恢复交互合同。
- [Copy Rules](uiux/COPY_RULES.md)：面向用户的状态与错误文案规则。
- [Design Tokens](uiux/DESIGN_TOKENS.md)：视觉 token 与响应式约束。

## 详细技术方案

- [V1 Technical Solution Proposal](engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md)：整体架构、三服务职责、技术路线和关键决策摘要。
- [V1 Detailed Technical Design](engineering/V1_DETAILED_TECHNICAL_DESIGN.md)：跨服务端到端详细设计和实施边界。
- [Service, Middleware and Operations Design](engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md)：Web/API/Worker、PostgreSQL、Redis、MinIO、异步控制面、HA、恢复和运维设计。
- [Data and Interface Contract Design](engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md)：逻辑表、约束、REST/SSE、内部 Worker 协议、receipt、上传与删除合同。
- [Frontend Technical Design](engineering/V1_FRONTEND_TECHNICAL_DESIGN.md)：前端路由、状态、数据访问、离线草稿、响应式与降级实现合同。
- [Reliability Budget](engineering/RELIABILITY_BUDGET.md)：DataSafetyGate、可用性适用条件、恢复与故障门。
- [Performance Budget](engineering/PERFORMANCE_BUDGET.md)：H0 基准输入、指标、容量和升级触发器。
- [Decision Log](decisions/DECISION_LOG.md)：适用 ADR、状态、owner 与待批准决策入口。

## 系统决策 Prompt

- [System Decision Prompts](ai/SYSTEM_DECISION_PROMPTS.md)：各阶段用于系统判断和大模型候选决策的 Prompt family、D/S/H 权责、输入输出 Schema、评测、激活、撤销与效果保障。

该文档只定义系统决策 Prompt，不包含小说正文、改文或包装文案写作 Prompt。模型只产生候选；确定性规则、必要人工确认和服务端二次校验共同形成权威状态。

## Review 与自评估

- [Technical Solution Adversarial Review](engineering/V1_TECHNICAL_SOLUTION_ADVERSARIAL_REVIEW.md)：基于当前实现现状的挑刺审查、整改闭环和仍待实现的生产门。
- [Technical Solution Evaluation](engineering/V1_TECHNICAL_SOLUTION_EVALUATION.md)：可持续性、可扩展性、高可用、高性能和实施成熟度评估。

## 建议阅读顺序

1. 先读 Package Intake 与 Evidence Policy，确认当前批准范围。
2. 再读 Product Brief、PRD 增补和 Release Capability Matrix，确认版本范围与 UIUX。
3. 阅读 Technical Solution Proposal，再进入四份详细技术设计。
4. 涉及 AI 决策时读取 System Decision Prompts；涉及实现时同时读取适用 ADR、可靠性预算、性能预算和实施计划。
5. 最后用 Adversarial Review 与 Technical Solution Evaluation 检查“设计已闭合”是否被误写成“实现已完成”。
