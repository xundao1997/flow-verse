# FlowVerse V1 数据模型与接口合同详细设计（评审稿）

## 0. 状态、权威与交付边界

**状态：`IN_REVIEW / PROPOSED`。**

本文是 PostgreSQL 逻辑 Schema、对象元数据、REST/SSE、API↔Worker 和 AI 执行绑定的合同候选。它足以用于评审后生成物理 DDL、Alembic migration、OpenAPI 和 TypeScript client，但本文本身不批准或实现它们。

- 产品字段和状态含义来自 Product Brief、PRD 增补、批准的原 PRD 与 UIUX；本文不得增加用户必须确认的新业务事实。
- 模型只产生 candidate；服务端确定性系统和必要人类确认共同形成权威状态。
- 表名、列名、URL、HTTP status、错误码、枚举、索引和约束在最终 Schema/API ADR 获批前仍可调整；调整必须同步所有消费者。
- V1 只建小说域。本文不包含金融 instrument、market data、research、portfolio、backtest、vector 或 time-series 表/接口。
- Redis 不保存本文任何权威记录；MinIO 只通过 logical object/version adapter 使用；Worker 不直接读写本文业务表。

本文件是本详细设计包中数据/协议的唯一明细源；[总体设计](V1_DETAILED_TECHNICAL_DESIGN.md) 和 [前端设计](V1_FRONTEND_TECHNICAL_DESIGN.md) 只引用，不另造同名字段。

## 1. PostgreSQL 建模规则

### 1.1 物理组织建议

推荐一个 PostgreSQL database、一个有序 Alembic head，并按唯一 data owner 使用以下 database schema：

`identity_access`、`task_lifecycle`、`creative_reference`、`creative_content`、`review_compliance`、`execution_control`、`release_cycle`、`feedback_decision`、`governance_ops`。

每个 schema 的 migration 内容归同名模块；migration graph 仍只有一个 head。模块不能直接查询另一 schema 的表，跨 owner 由 application use case 调公共入口；允许数据库 FK/unique 作为完整性防线，但跨 owner 删除使用显式用例和 `RESTRICT`，不使用跨聚合 `ON DELETE CASCADE` 偷偷清理历史。

### 1.2 通用类型与列

| 语义 | PostgreSQL 建议 | 规则 |
|---|---|---|
| 主键/稳定引用 | `uuid` | 应用生成 UUIDv7 候选；不得把顺序 ID 暴露为权限边界；具体生成库待批 |
| revision | `bigint NOT NULL DEFAULT 1` | 只在可变聚合 root 上递增；命令带 expectedRevision |
| 时间 | `timestamptz` | 服务端写 UTC instant；另存用户/业务时区 ID，不存无时区时间 |
| 短枚举 | `text` + named `CHECK` | 未批准前不使用 PostgreSQL enum；新增值是合同变化并要安全客户端行为 |
| 长文本 | `text` | 正文/Prompt/output 必须有应用层及批准的最大长度；不进普通日志 |
| hash | `char(64)` | 小写 SHA-256；check `[0-9a-f]{64}`；ETag 不可替代 |
| 金额 | `numeric(20,6)` + ISO currency `char(3)` | 不用 float；估算、预留和实际分开 |
| token/计数 | `bigint` | 非负 check；Unknown 不伪造为 0 |
| typed manifest | `jsonb` | 必须伴随 `schema_version`、canonical hash；只用于不可变结构/低频扩展 |
| content locator | `text` 或结构列 | 行/段/字段/对象版本定位；不可包含 presigned URL |
| IP/UA 安全元数据 | `inet`/受限 text/hash | 按隐私政策最小化；不成为普通审计必填全文 |

可变 root 通用列：`id`、`revision`、`created_at/by`、`updated_at/by`。不可变 record 通用列：`id`、`schema_version`、`created_at/by`，没有 `updated_at`；更正以 `replaces_id/corrects_id/supersedes_id` 新增记录。正式记录禁止普通 `UPDATE/DELETE`，通过 runtime role 权限、repository 和必要的防御性 trigger/constraint 共同保护；trigger 的精确方案需在 DDL 审批时确认。

### 1.3 数据分类与 JSONB 边界

- 关系列保存所有需过滤、排序、约束、授权、连接或形成状态机的字段。
- JSONB 仅用于不可变 manifest、family-specific typed payload、外部原始但已验证的有限 metadata、评测结果细节和审计差异摘要。
- 禁止把 Task/Cycle/status/role/permission/revision/cost/available capability 等核心字段塞进通用 JSONB。
- 每个 JSONB 有 Pydantic/JSON Schema、`schema_version`、`additionalProperties` 规则和迁移/旧版只读策略。
- 原始对象字节在 ObjectStore；正文和正式小说版本在 PG，不把 MinIO 当唯一事实源。

## 2. 逻辑表结构总览

下列 `PK/FK/UQ/CK/IDX` 分别表示主键、外键、唯一、检查和索引。所有 FK 默认 `ON DELETE RESTRICT`；仅纯内部、可重建明细在 owner 明确批准时才可 cascade。

### 2.1 `identity_access`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `account` | `id uuid PK`; `login_name text`; `login_name_normalized text`; `display_name text`; `role text`; `status text`; `must_change_password bool`; `failed_login_count int`; `locked_until timestamptz?`; `revision`; audit columns | UQ `login_name_normalized`; CK role=`USER/ADMIN`; CK status=`ACTIVE/LOCKED/DISABLED`; CK failed>=0; IDX status/locked_until | root 可变；禁用不删除身份引用 |
| `password_credential` | `id`; `account_id FK`; `password_hash text`; `algorithm text`; `parameters jsonb`; `credential_version int`; `valid_from`; `revoked_at?`; `created_at/by` | UQ `(account_id,credential_version)`; partial UQ one non-revoked credential/account; hash never returned | append/revoke；不进180天内容审计 |
| `session` | `id`; `account_id FK`; `session_token_hash char(64)`; `role_snapshot`; `created_at`; `last_seen_at`; `idle_expires_at`; `absolute_expires_at`; `revoked_at/reason?`; `csrf_secret_hash`; `revision` | UQ token hash; CK expiry order; IDX `(account_id,revoked_at)`、`idle_expires_at`; raw token absent | mutable heartbeat/revoke；到期清理窗口待安全批准 |
| `debug_access_grant` | `id`; `admin_account_id FK`; `target_task_id`; `scope_codes text[]`; `reason`; `approved_by`; `valid_from/to`; `revoked_at`; `created_at` | CK admin actor by application+D2; CK valid_to>valid_from; IDX active range/target | append/revoke；授权事实进180天非内容审计 |

不建公开 registration/invitation/password-reset/MFA/SSO/team 表。账号预置或受控管理创建仍需明确安全流程；管理员不能创建可冒充当前 user 的 session。

### 2.2 `task_lifecycle`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `novel_task` | `id`; `owner_account_id FK`; `name`; `lifecycle_status`; `control_status`; `visibility_status`; `deletion_status`; `current_cycle_id?`; `next_cycle_number bigint`; `revision`; timestamps | CK 四状态各自闭合集； CK next_cycle_number>=1; IDX owner+updated; partial IDX active; current_cycle 由 use case 维护 | aggregate root；删除 intent 后立即按批准状态不可访问 |
| `stage0_draft` | `id`; `task_id FK`; `draft_kind`; `payload jsonb`; `payload_schema_version`; `revision`; timestamps | UQ `(task_id,draft_kind)`; CK kind=`CREATION/OPERATION`; payload Schema；IDX task | 可变草稿；不能作为正式 baseline |
| `creation_baseline_version` | `id`; `task_id FK`; `version_no`; 逐字段结构列/有限 typed json；`replaces_id?`; `confirmed_by/at`; `canonical_hash` | UQ `(task_id,version_no)`、hash/task；字段必须逐项映射 PRD 增补3.1；replacement同task | append-only；任务存续期不可覆盖 |
| `operation_validation_baseline_version` | `id`; `task_id`; `creation_baseline_id FK`; `version_no`; 平台/账号标识、release scope、metric/timezone/observation/data completeness、cycle budget、comparison/prohibited claims、manual-time baseline 等结构字段；`rule_version_id`; replacement/confirm/hash | UQ task+version；exact field allocation 来自PRD增补3.2；CK时区非空、观察点有序；不复制task级总预算 | append-only；一轮验证期间冻结；替换传播影响 |
| `task_transition` | `id`; `task_id`; `transition_type`; `from/to lifecycle/control/visibility/deletion`; `reason`; `command_receipt_id`; actor/time | IDX task+created_at；transition闭合由domain+D2验证 | append-only activity proof |
| `baseline_dependency_invalidation` | `id`; `task_id`; `baseline_ref`; `dependent_ref/type`; `reason_code`; `status`; `detected_at`; `resolved_at?` | UQ baseline+dependent+reason active；IDX unresolved | append/resolve；帮助显式stale传播，不是第二状态源 |

`creationReady` 和 `operationReady` 是服务端 query/capability 结果，不建含糊 `stage0_complete` 列。前者只需当前确认 CreationBaseline，后者需两部分及到期规则有效。

### 2.2A `task_lifecycle` P01 Bot 最小资源

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `bot_conversation` | `id`; `account_id`; `task_id?`; `scope_type`; `context_revision`; `status`; timestamps | UQ active account+scope；scope只能global/task；IDX account/updated | root；Bot故障不阻断task入口 |
| `bot_message` | `id`; `conversation_id`; `sender_type`; `content_text`; `client_message_id?`; `execution_id?`; `status`; `created_at` | UQ conversation+client_message_id；sender=`USER/BOT/SYSTEM`; IDX conversation/time | append-only；BOT仅candidate响应 |
| `bot_action_card` | `id`; `message_id`; `action_descriptor_id`; `target_route_id`; `target_ref?`; `context_revision`; `expires_at`; `status` | 只能引用服务端允许的导航descriptor；过期/revision不符失效 | append/expire；只导航owning page，不执行mutation |
| `bot_unapplied_draft` | `id`; `conversation_id`; `source_message_id`; `draft_type`; `owning_route_id`; `payload_schema_version`; `payload`; `context_revision`; `status`; timestamps | UQ source+draft type；strict schema；不能满足正式字段或直接写业务owner | candidate；用户在owning page显式应用/编辑/丢弃 |

### 2.3 `governance_ops` 对象目录（跨域二进制 owner）

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `stored_object` | `id`; `owner_account_id`; `task_id?`; `purpose`; `lifecycle_status`; `current_version_id?`; `retention_class`; `revision`; timestamps | CK purpose closed；CK lifecycle=`UPLOADING/QUARANTINED/VERIFYING/VERIFIED/PROCESSING/PARTIAL/COMMITTED/REJECTED/DELETING/DELETED`; IDX task/status | root；不含bucket/key |
| `stored_object_version` | `id`; `stored_object_id`; `version_no`; `sha256?`; `size_bytes?`; `media_type?`; `provider_locator_ciphertext`; `provider_version?`; `verified_at?`; `verification_status`; `created_at` | UQ object+version；UQ provider locator adapter scope；CK size>=0/hash；locator字段只允许adapter role | immutable；删除后只留允许的去重/ledger最小metadata |
| `upload_session` | `id`; `object_id/version_id`; `declared_name/type/size/hash?`; `max_bytes`; `expires_at`; `status`; `finalize_command_id?`; timestamps | UQ active session/object version；CK expiry、max>0；IDX expires/status | mutable至sealed；到期清理 |
| `object_verification` | `id`; `object_version_id`; `job_id`; `actual_sha256/size/media_type`; `validator_version`; `status`; `reason_codes`; `created_at` | UQ successful verification/version；hash/size CK；manifest外metadata拒绝 | append-only |
| `object_reference` | `id`; `object_version_id`; `owner_module`; `owner_record_id`; `purpose`; `commit_watermark?`; `closed_watermark?`; `created_at`; `closed_at?` | UQ owner_module+record+purpose active；B2启用时UQ/non-null monotonic commit watermark且close>commit；IDX object_version/watermark；不允许任意owner string未注册 | append/close；B2 checkpoint与ledger覆盖窗口结束前不得hard delete引用历史 |

ObjectStore 的 bucket/key/version 不进入其他 schema；下载与 Worker 输入临时 grant 不耐久保存 raw URL，只记录 grant type/object/version/expiry/actor 的安全审计摘要。

### 2.4 `creative_reference`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `reference_asset` | `id`; `task_id`; `object_version_id FK`; `display_name`; `source_type`; `source_description`; `rights_status`; `allowed_usage`; `processing_status`; `revision`; timestamps | UQ task+object version；CK rights/usage/status；IDX task/status | root；rights变化新revision并失效依赖 |
| `reference_extraction_version` | `id`; `reference_id`; `version_no`; `parser_name/version`; `source_object_hash`; `text_content?`; `structure_json?`; `usable_ratio numeric`; `missing_ranges jsonb`; `status`; `created_at` | UQ ref+version；CK ratio 0..1；hash匹配object；IDX status | append-only；大中间产物可object ref |
| `reference_fragment` | `id`; `extraction_version_id`; `ordinal`; `locator`; `text_content`; `text_hash`; `character_count`; `risk_status`; `created_at` | UQ extraction+ordinal；CK count/hash；IDX extraction, risk；可批准全文/结构搜索索引 | append-only |
| `reference_selection` | `id`; `task_id`; `execution_preview_id?`; `fragment_id`; `selection_type`; `selected_by`; `reason?`; `created_at` | UQ execution/fragment/type；CK type=`USER_FIXED/SYSTEM_SUGGESTED`; manifest冻结后不改 | append-only |
| `reference_use` | `id`; `execution_binding_id`; `reference_id`; `fragment_id`; `usage_role`; `input_locator`; `created_at` | UQ binding+fragment+role；IDX ref/binding；必须来自批准selection | append-only实际使用链 |

PDF 截图/页面图像不落 `reference_fragment`，不 OCR，不进入 `reference_use`。reference deletion 先用 `object_reference/reference_use` 计算影响，再按任务删除/单参考规则处理。

### 2.5 `creative_content`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `creative_object` | `id`; `task_id`; `object_type`; `logical_key`; `title`; `current_formal_version_id?`; `revision`; timestamps | UQ task+type+logical_key；CK type=`STORY_BIBLE/CHARACTER/OUTLINE/CHAPTER`; IDX task/type | stable root |
| `draft_revision` | `id`; `creative_object_id`; `revision_no`; `base_formal_version_id?`; `content_format`; `content_schema_version`; `content_text`; `source`; `saved_by/at`; `supersedes_draft_id?` | UQ object+revision_no；CK source=`USER/AUTOSAVE/RECOVERY`; IDX object+saved_at | append；可按获批策略压缩，未同步草稿另在浏览器 |
| `candidate_set` | `id`; `creative_object_id`; `set_kind`; `execution_request_id?`; `based_on_formal_version_id?`; `status`; `selected_primary_candidate_id?`; `revision`; timestamps | set与object/task一致；一个set只属于一次用户批次或一次execution；selected candidate必须属于本set；IDX object/status | stable batch root；`selected_primary_candidate_id` 是主候选唯一事实，选择变化经正式command/revision留痕 |
| `candidate` | `id`; `candidate_set_id`; `creative_object_id`; `candidate_kind`; `based_on_formal_version_id?`; `execution_output_id?`; `input_manifest_id?`; `content_format/schema_version/text`; `status`; `revision`; timestamps | candidate必须与set同object；AI candidate必须execution output；IDX set/object/status | mutable review state，正文不覆盖；不保存第二个primary flag；正式化不删除 |
| `formal_object_version` | `id`; `creative_object_id`; `version_no`; `source_candidate_id`; `content_format/schema_version/text`; `canonical_hash`; `confirmed_by/at`; `replaces_id?` | UQ object+version；UQ source candidate formalized once；hash CK；same-object replacement | immutable |
| `content_snapshot` | `id`; `task_id`; `snapshot_no`; `creation_baseline_id`; `memory_status`; `releasability`; `manifest_schema_version`; `manifest_hash`; `confirmed_by/at` | UQ task+snapshot_no/hash；releasability check；IDX task+confirmed | immutable complete manifest root |
| `content_snapshot_item` | `snapshot_id`; `creative_object_id`; `formal_version_id`; `object_type`; `ordinal` | composite PK snapshot+object；UQ snapshot+ordinal per type；formal version必须属于object/task | immutable |
| `memory_change_set` | `id`; `task_id`; `source_snapshot_id`; `based_on_memory_version_id?`; `status`; `execution_binding_id?`; `created_at` | UQ source snapshot current set；CK status；AI output仅candidate | append/state until human confirmation |
| `memory_change_item` | `id`; `change_set_id`; `change_type`; `fact_key`; `old/new_value`; `evidence_refs jsonb`; `criticality`; `status` | closed change types；evidence schema；IDX change_set/status | append/resolution |
| `work_memory_version` | `id`; `task_id`; `version_no`; `source_change_set_id`; `manifest_hash`; `confirmed_by/at` | UQ task+version；UQ source change set；immutable | immutable |
| `work_memory_fact` | `memory_version_id`; `fact_key`; `fact_type`; `value_text/json?`; `source_formal_version_id`; `status` | composite PK memory+key；exactly one typed value；source same task | immutable manifest item |

正文列表查询禁止默认返回 `content_text`。ContentSnapshot 每次包含全部当前正式对象 version ref；snapshot 本身不复制各正文。

### 2.6 `review_compliance`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `review_run` | `id`; `task_id`; `target_type/id/revision`; `review_type`; `rubric_version_id`; `execution_binding_id?`; `status`; `started/completed_at`; `input_hash` | UQ target+revision+type+rubric+current run policy；IDX target/status | append-only run；stale另标记录 |
| `review_finding` | `id`; `review_run_id`; `criterion`; `category`; `severity_candidate`; `authoritative_severity?`; `locator`; `statement`; `evidence_refs`; `status`; `created_at` | evidence Schema；closed severity；IDX run/status/severity | append/resolution；模型severity非最终block |
| `finding_resolution` | `id`; `finding_id`; `resolution_type`; `reason`; `resolved_by/at`; `replacement_target_ref?` | UQ active resolution/finding；重要风险需reason；BLOCK不可接受绕过 | append-only |
| `semantic_finding_candidate` | `id`; `task_id?`; owning_target_type/id/revision；family_id；`execution_output_id`; input_manifest_id/hash；trusted_envelope_schema_version/hash；status；validation_status；family_payload_schema/version；created_at；stale_at/reason? | FK `execution_output_id`必须指向持有canonical `semantic-candidate-envelope/v1`的不可变output，candidate所存schema/hash必须与该output一致且可重算；UQ output+family+target revision；status=`CANDIDATE/ABSTAIN/NEEDS_HUMAN_REVIEW`; invalid/stale不可采用；IDX target/status | immutable candidate version；重跑新记录；不复制或另造第二份可信envelope |
| `semantic_finding_item` | `id`; `candidate_id`; `ordinal`; finding_code；severity_candidate；label；action_suggestion_id?；rationale_summary；unknowns/alternatives typed payload | UQ candidate+ordinal；closed taxonomy/action；不得保存权威PASS/BLOCK | immutable |
| `semantic_evidence_ref` | `id`; `finding_item_id`; source_id/version_id/locator；relation；source_manifest_item_hash | UQ finding+source/version/locator/relation；必须在input manifest且hash一致 | immutable locator，不复制来源正文 |
| `semantic_candidate_human_review` | `id`; `candidate_id`; `review_revision`; outcome；edited_payload?；reason_codes；requested_evidence?；reviewed_by/at | UQ candidate+review revision；outcome=`ACCEPT_FOR_D2/EDIT_FOR_D2/REJECT/REQUEST_EVIDENCE`; candidate stale/invalid时不能accept | append-only；接受仍不formal，D2重验 |
| `agent_disagreement` | `id`; `target_ref`; `stance_a/b`; `evidence_a/b`; `status`; `human_resolution?`; actor/time | evidence required；IDX target/unresolved | append/resolution |
| `risk_acceptance` | `id`; `target_ref`; `finding_id`; `accepted_scope`; `reason`; `accepted_by/at`; `expires_at?` | only eligible non-BLOCK；UQ finding/scope active | immutable/expiry |
| `compliance_check` | `id`; `target_ref/revision`; `stage`; `policy_version_id`; `semantic_candidate_ref?`; `validator_version`; `created_at` | CK stage=`PRE_GENERATION/POST_GENERATION/PRE_RELEASE`; IDX target/stage | immutable input/validator record |
| `compliance_decision` | `id`; `check_id`; `decision`; `reason_codes`; `required_human_review`; `human_review_ref?`; `decided_at`; `decision_hash` | decision=`PASS/HUMAN_REVIEW/BLOCK`; BLOCK无override；human ref when required | immutable authority record |

Unified Review 是 query projection，不建覆盖来源记录的万能 result 表。

### 2.7 `execution_control`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `execution_preference_version` | `id`; `task_id`; `creation_baseline_id`; `version_no`; preferred model/profile/agent/candidate-count/language-strength 等边界内未来默认值；`canonical_hash`; `confirmed_by/at`; `replaces_id?` | UQ task+version；每个值必须被当前 CreationBaseline 允许；IDX task/version | append-only；不是基线/权限/本次实际值 |
| `execution_preview` | `id`; `actor_id`; `task_id?`; `preview_kind`; `source_execution_id?`; `source_lane_no?`; `replaces_attempt_id?`; `execution_purpose`; `workload_type`; `input_manifest_id`; `lane_selection_manifest_ref/hash`; `evaluation_authorization_receipt_ref/hash?`; agent/candidate selections；price/policy versions；estimate/ceiling；`revision`; `expires_at`; `status` | kind=`INITIAL/RETRY/FALLBACK`；INITIAL禁止三个source字段且manifest lane恰为连续1..N；RETRY/FALLBACK要求三者齐全、`0<sourceLane<=sourceExecution.initialLaneCount`、replaced attempt属于该source execution/lane，manifest恰含一个`laneNo=sourceLane`而不重编号；purpose与source一致；每lane冻结model/profile、PromptConfig/EvaluationBinding；BUSINESS role为空、每lane要求匹配`environment+family+scope+modelProfile`当前activation且N<=3；EVALUATION要求有效`OFFLINE_EVALUATION`或`SHADOW_EVALUATION_CONSENT` receipt并按其EvaluationBinding有界plan把provider lane正交标记`evaluationCallRole=TARGET|JUDGE`与可空`evaluationArm=CANDIDATE|CONTROL`：TARGET必须有arm且只匹配真实PromptConfig；typed HUMAN/NO_AI baseline只作为CONTROL evidence并禁止provider lane；JUDGE arm为空且匹配冻结judge配置与basis-specific dependency selector，human-only禁止JUDGE lane，所有lane禁止借用activation；Shadow还须匹配用户task/execution/input scope、增量费用/slot和rollout authority/allowlist；UQ active preview/intent；price/budget/data-license CK；IDX actor/purpose/task/status | mutable until authorized/expired；kind、purpose、source、role、arm或lane identity不可原地转换 |
| `input_manifest` | `id`; `task_id?`; `manifest_type`; `schema_version`; `items jsonb`; `canonical_hash`; `data_classification`; `excluded_items`; `created_at` | UQ hash+scope；strict manifest schema；screenshots/provider secrets forbidden | immutable |
| `execution_binding` | `id`; `preview_id`; `lane_no`; `execution_purpose`; `evaluation_call_role?`; `evaluation_arm?`; `prompt_config_ref/hash`; `evaluation_binding_ref/hash`; `evaluation_authorization_receipt_ref/hash?`; `eligibility_assessment_ref/hash/revision?`; `activation_revision?`; `input_manifest_id/hash`; `judge_dependency_selector_manifest_ref/hash?`; resolved provider/model/profile/adapter refs+hash；sampling/reasoning/parameter manifest ref+hash；typed variable manifest ref+hash；context-assembly/retrieval snapshot ref+hash；output-schema ref+hash；policy/price/budget/data-scope refs+hash；`deadline_at`; `schema_version`; `canonical_hash`; `created_at` | UQ `(preview_id,lane_no)`；lane与preview manifest一一对应；BUSINESS要求role/arm为空、activation+最新eligible assessment并禁止evaluation authorization；EVALUATION要求role=`TARGET/JUDGE`、同一有效typed authorization receipt+EvaluationBinding且禁止activation/eligible-assessment。provider TARGET要求arm=`CANDIDATE|CONTROL`并只匹配实际PromptConfig；typed baseline不得创建provider lane。JUDGE要求arm为空并匹配冻结judge配置：DIRECT selector只允许candidate artifact+rubric/schema且无control/blind/order；PROMPT_ONLY selector覆盖同一authorization/run内两个provider arm、artifact schema与order-swap；BASELINE_GATE selector覆盖candidate artifact与typed baseline artifact/authority receipt且无control ModelCall；FACTORIAL selector服从冻结factor/control plan。所有selector都不能伪造未来artifact hash。OFFLINE/SHADOW的scope/slot/cost/output owner逐项匹配authorization manifest；resolved values逐项匹配对应lane定义与当前policy；strict canonical manifest；pre-call immutable | immutable per-lane call-before fact；由一个attempt唯一引用；任一单次解析值、基础输入或dependency selector变化建立新binding；JUDGE实际artifact/baseline refs/hash只在依赖终态后写入ModelCall，不回写binding |
| `execution_request` | `id`; `origin_preview_id`; `actor_id`; `task_id?`; `execution_purpose`; `initial_lane_count`; `workload_class`; `status`; `priority`; `deadline_at`; `cancel_requested_at?`; `revision`; timestamps | UQ origin preview；purpose与preview/binding一致；BUSINESS lane count 1..3；EVALUATION lane count精确匹配EvaluationBinding的有界TARGET/JUDGE plan；EVALUATION使用独立pool/quota/cost且不得占业务candidate/formal owner；CK status/deadline；partial UQ active paid slot via slot table；IDX purpose/status/priority/created | aggregate root；purpose/lane count创建后不可改；不保存可被retry覆盖的单数binding |
| `execution_attempt` | `id`; `execution_id`; `binding_id`; `lane_no`; `attempt_in_lane`; `attempt_kind`; `replaces_attempt_id?`; `reason`; `status`; `started/finished_at`; `outcome_class`; `fencing_high_watermark` | UQ `(execution_id,lane_no,attempt_in_lane)`；UQ binding；kind=`INITIAL/RETRY/FALLBACK`；INITIAL要求attempt_in_lane=1且无replaces，RETRY/FALLBACK只替代同execution+lane的前一attempt并使用新preview/new binding；binding lane/purpose与attempt一致；binding存在后才能claim；IDX execution/lane/status | append/state to terminal；一个attempt只代表一个model lane，不混用模型或binding |
| `execution_step` | `id`; `attempt_id`; `step_no`; `role_code`; `agent_template_version`; `status`; times | UQ attempt+step；closed role/status；IDX attempt | append/state |
| `model_call` | `id`; `step_id`; `call_no`; `call_intent_id`; `execution_purpose`; `evaluation_call_role?`; `evaluation_arm?`; `eligibility_assessment_ref/hash/revision?`; `evaluation_authorization_receipt_ref/hash?`; `resolved_call_input_manifest_ref/hash`; `provider_request_ref?`; `model_exact_version`; `parameters_hash`; `request_hash`; `call_start_status`; `authorized_at`; `authorization_expires_at`; `provider_idempotency_strategy`; `provider_idempotency_capability_version`; `provider_idempotency_key_version/scope?`; `provider_idempotency_key_ciphertext_or_ref?`; `provider_idempotency_key_hash?`; `dispatch_confirmed_at?`; terminal `status`; token counts nullable；provider latency；error taxonomy；times | UQ `(step_id,call_no)`、`call_intent_id`；UQ provider request ref if supplied；purpose/role/arm与attempt/binding一致；BUSINESS role/arm为空并冻结JIT时最新eligible assessment；EVALUATION冻结同一评测授权且assessment为空，provider TARGET要求CANDIDATE/CONTROL arm，JUDGE arm为空。BUSINESS/TARGET的resolved call input必须由binding冻结的输入确定性产生；DIRECT JUDGE只需candidate receipt；PROMPT_ONLY需两个provider arm与order-swap receipts；BASELINE_GATE需candidate receipt+typed baseline artifact/authority receipt且没有control ModelCall；FACTORIAL按冻结plan取证。manifest逐项引用同一authorization/run内所需artifact或baseline ref/hash/receipt并匹配selector/schema/order；terminal status闭合并包含只能由删除reconciliation proof设置的`OUTCOME_UNKNOWN_NO_PAYLOAD`，它不声称provider未处理数据；CK exact-key strategy、expiry、nonnegative counts；明文key/secret不落日志或公开DTO | API在JIT call-start事务中先插入不可变意图并冻结本次真实调用输入、对应purpose/role/arm权威依据与可重建/可解密exact-key策略；随后只允许受控状态追加/终结，已完成事实保留 |
| `execution_output` | `id`; `model_call_id`; `output_type`; `schema_version`; `raw_object_version_id?`; `parsed_model_payload jsonb?`; `raw_output_hash`; `canonical_envelope jsonb?`; `envelope_schema_version?`; `envelope_hash?`; `validator_version`; `validator_result jsonb`; `validation_status`; `created_at` | exactly one/bounded raw storage route；UQ call+output type/hash；语义候选必须持久化严格17字段、`additionalProperties=false`的`semantic-candidate-envelope/v1`且envelope hash可重算；可信字段由executor写入，`modelPayload`与可信metadata边界固定；非语义输出按独立schema且不得冒用该envelope名 | immutable；validator/output事实不回写binding |
| `cost_ledger_entry` | `id`; `execution_id`; `attempt_id?`; `model_call_id?`; `entry_type`; `amount`; `currency`; `token/input units?`; `price_version_id`; `certainty`; `created_at` | amount>=0；entry type estimate/reserve/actual/release/adjustment；adjustment not overwrite | append-only ledger |
| `execution_slot` | `id`; `scope_type`; `scope_id`; `slot_type`; `execution_id`; `status`; `acquired_at`; `released_at?`; `revision` | partial UQ active `(scope_type,scope_id,slot_type)`；user paid/task business guards | state with history via audit |
| `durable_job` | `id`; `job_type`; `execution_id?`; `attempt_id?`; `object_version_id?`; `export_request_id?`; `maintenance_type?`; `deletion_request_id?`; `recovery_checkpoint_id?`; `workload_class`; `pool_key`; `fairness_key`; `status`; `available_at`; `priority`; `attempt_count`; `claim_skip_count`; `job_revision`; `lease_fencing_counter`; `retired_at/reason?`; `payload_manifest_ref/hash`; timestamps | `AI_EXECUTION`恰有execution+attempt且attempt属于execution；`DOCUMENT_PROCESSING`恰有object_version；`EXPORT_GENERATION`恰有export_request；`MAINTENANCE`只允许`DELETION_RECONCILIATION/RECOVERY_CHECKPOINT_BUILD`并恰有对应request/checkpoint；四组互斥且创建后不可换型；UQ semantic typed owner；IDX claim `(pool_key,status,available_at,priority,created_at)`；CK attempts/skip>=0；retire reason闭合集 | API-owned discriminated root；typed context固定后不可改；维护不是任意脚本入口；retire只由诊断/人工恢复用例决定并留receipt |
| `job_lease` | `id`; `job_id`; `worker_id`; `lease_purpose`; `fencing_token`; `leased_at/expires_at`; `heartbeat_at`; `last_heartbeat_request_id/sequence/digest?`; `last_heartbeat_result_job_revision/expires_at?`; `status`; `release_reason?` | purpose=`WORK/DELIVERY_RECOVERY/DELETION_DISPOSITION`；UQ job+fencing；partial UQ active lease/job；token monotonic in locked job；heartbeat sequence单调，同requestId+digest重放同一revision/expiry，异digest冲突，旧sequence拒绝。DELIVERY_RECOVERY只可在已有可验证RESULT_BUFFERED record、无report receipt且原WORK lease失效后签发；DELETION_DISPOSITION只可在ledger intent+tombstone已耐久、匹配pre-barrier `CALL_START_COMMITTED`、普通WORK已fence且该intent尚无buffer/disposition receipt时签发 | append/state；historical fencing与心跳outcome-unknown proof；两种特殊lease均不得调用provider或生成第二result，disposition仅可把该intent已有outcome写入删除隔离区并报告丢弃 |
| `job_report_receipt` | `id`; `job_id`; `job_context_ref/hash`; `call_intent_id?`; `report_type`; `request_digest`; `producer_lease_id/fencing_token/job_revision`; `acceptance_proof_kind`; `acceptance_job_id?`; `acceptance_lease_id/fencing_token/job_revision?`; `acceptance_transaction_revision?`; `post_report_job_revision?`; `report_key`; `delivery_record_ref/hash?`; `result_hash?`; `no_payload_proof_ref/hash?`; `accepted_status`; `deletion_request_id?`; `ledger_cursor?`; `tombstone_revision?`; `created_at` | UQ `(job_id,report_key)`；同key同digest返回同receipt、异digest冲突；acceptance kind=`WORK_LEASE/DELIVERY_RECOVERY_LEASE/DELETION_DISPOSITION_LEASE/DELETION_RECONCILIATION`，并保留原producer proof。type=`PROGRESS/RESULT/FAILURE/NO_PAYLOAD_DISPOSITION`；前三类按相应lease与delivery规则。NO_PAYLOAD仅由DELETION_RECONCILIATION生成，冻结callIntent、deletion/ledger/tombstone、全部相关WORK/DISPOSITION lease与写grant均失效、固定index HWM完整无record且无并发处置的proof，delivery/result为空且status=`NO_PAYLOAD_DISPOSITION_ACCEPTED`；它只证明系统无可恢复本地payload，不证明provider未处理数据。stale/不匹配proof rejected | immutable report/处置幂等proof；progress/pure-failure/no-payload receipt不授权INT-009，discard/no-payload均不创建业务output/candidate/formal事实 |

`FOR UPDATE SKIP LOCKED` 仅在 API persistence 对 `durable_job` claim query 使用。Worker 只认识内部 DTO，不获得数据库 URL。`pool_key`隔离付费AI、对象处理、导出和上述两个封闭维护 subtype 的容量；`fairness_key`、有界 aging 与带 jitter 的空领取退避避免高优先级或空轮询长期饿死其他类，精确权重/间隔必须由 H0 测量后批准。达到获批 attempt/age/unknown-outcome 条件的 job 不再自动回到 `AVAILABLE`，而进入 `WAITING_DIAGNOSIS/RETIRED` 候选状态和人工诊断环。DeliveryStore locator 可在 `governance_ops.stored_object`，业务权威只在 result/discard receipt、owner outputs 和必要的非内容成本/审计记录；其满载、不可写、校验失败或保留到期必须使对应 Worker 停止 claim 并显式降级，不能无终态处置地丢弃尚未获 API receipt 的结果。

高级设置只产生 `execution_preference_version`。它绑定当前 CreationBaseline 并在其允许池/强度/数量边界内给未来执行提供默认偏好；越界请求返回 `BASELINE_REPLACEMENT_REQUIRED` 并导航 Stage0，不能由设置页静默扩大。首次授权把最多三个已选模型映射为稳定`lane_no=1..N`，在同一事务创建一个execution root、每lane独立的PromptConfig/Evaluation/ExecutionBinding、`INITIAL attempt_in_lane=1`与job；各lane共享冻结input manifest、用户/任务slot和批次总预算上限，但保留逐lane预算/费用证据。每次retry/fallback/model switch必须先确认只针对原lane的新preview，再创建同lane递增`attempt_in_lane`的新binding/attempt/job并引用被替代attempt；不能把失败lane重试解释为新的并行候选，也不能在一个binding/attempt中混用两个模型。`candidate_set.execution_request_id`聚合同一批次各lane成功候选并保留各自output lineage。每次D01/binding固化实际模型、Agent、候选数和语言强度，不能只引用“当前偏好”或复用旧binding；request只保存起始意图，不在重试时改写起源。

### 2.8 `release_cycle`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `packaging_candidate` | `id`; `task_id`; `based_on_snapshot_id`; `source`; `execution_output_id?`; title/summary/category/tags/cover_direction；`status`; `revision`; timestamps | AI source需output；字段长度/closed category rules；IDX task/status | candidate mutable；生成workload非系统决策Prompt |
| `packaging_version` | `id`; `task_id`; `version_no`; `source_candidate_id`; fields；`rule_version_id`; `canonical_hash`; `confirmed_by/at` | UQ task+version；UQ candidate formalized once | immutable |
| `release_plan` | `id`; `task_id`; `content_snapshot_id`; `packaging_version_id`; `operation_baseline_id`; `platform_rule_version_id`; `platform/account identifier`; scope；hypothesis/metrics/observation refs；`status`; `revision`; timestamps | all refs same task/current；UQ active ready plan optional；IDX task/status | mutable draft then immutable-confirmed version semantics |
| `release_plan_item` | `release_plan_id`; `formal_object_version_id`; `ordinal`; `release_scope` | composite PK；UQ plan+ordinal；chapter belongs snapshot | immutable after plan confirm |
| `actual_release` | `id`; `task_id`; `release_plan_id`; `effective_at`; platform/account；actual fields；`difference_class`; `external_actual_version_id?`; `confirmed_by/at`; `canonical_hash` | UQ release plan effective confirmation/command；normal eligibility checks；IDX task/effective | immutable external fact |
| `release_evidence` | `id`; `actual_release_id`; `evidence_type`; `object_version_id?`; `text_locator?`; `usage_scope`; `confirmed_by/at` | at least one locator；screenshot `HUMAN_ONLY`; never AI manifest | immutable |
| `external_actual_version` | `id`; `task_id`; `actual_release_id`; actual content/package fields/hash；`reason`; `confirmed_at` | UQ actual release；only material difference path | immutable，不成为FormalContent |
| `cycle` | `id`; `task_id`; `cycle_number bigint`; `actual_release_id`; `cycle_kind`; `status`; `validity_status`; `started_at`; `ended_at?`; `formal_decision_id?`; `revision` | UQ task+cycle_number；UQ actual_release；partial UQ one active/task；CK ended/status；IDX task/status | root；编号不复用/不重排 |
| `observation_point` | `id`; `cycle_id`; `point_type`; `planned_at`; `actual_reached_at?`; `status`; `metric_scope`; `revision` | UQ cycle+point type/time；timezone resolved from baseline；IDX due/status | mutable observation status |
| `external_event` | `id`; `cycle_id`; `event_type`; `occurred_at`; `recorded_at`; `fact_text`; `difference_scope`; `semantic_candidate_ref?`; `authoritative_impact`; `confirmed_by`; `corrects_id?` | closed event/impact；correction same cycle；IDX cycle/occurred | append-only |
| `cycle_validity_check` | `id`; `cycle_id`; `check_code`; `status`; `evidence_refs`; `evaluated_at`; `source_revision_hash` | UQ cycle+check+evaluation version；all PRD 7.6 items no N/A waiver | append evaluation；cycle validity D-owned |

ActualRelease 与 Cycle 在同一 PG 事务创建：锁 task、验证 revision/capability/唯一 active cycle、写 release、分配 `next_cycle_number`、写 Cycle/观察点/receipt/audit/event、更新 task，一次提交。

### 2.9 `feedback_decision`

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `feedback_draft` | `id`; `cycle_id`; `payload`; `schema_version`; `revision`; timestamps | UQ cycle current draft；typed schema | mutable；不进入分析 |
| `feedback_snapshot` | `id`; `cycle_id`; `snapshot_no`; `observation_point_id`; `confirmed_by/at`; `corrects_id?`; `canonical_hash` | UQ cycle+snapshot_no；correction same cycle；IDX cycle+confirmed | immutable |
| `feedback_metric_value` | `id`; `snapshot_id`; `metric_definition_ref`; `value_status`; `numeric_value?`; `unit`; `basis`; `observed_at`; `source`; `notes?` | exactly numeric iff `NUMERIC`; `TRUE_ZERO` distinct; closed five-state；UQ snapshot+metric | immutable |
| `feedback_comment` | `id`; `snapshot_id`; `text_content`; `source_locator`; `privacy_status`; `model_use_status`; `redacted_text?`; `confirmed_by/at` | raw/redacted separation；screenshot absent；model use closed；PII policy | immutable |
| `analysis_input_manifest` | `id`; `cycle_id`; `actual_release_ref/hash`; metric definitions；feedback/comment version refs；window；confounders；exclusions；allowed model input；`schema_version`; `canonical_hash`; `created_at` | UQ canonical hash/cycle；latest confirmed refs；screenshot object forbidden | immutable |
| `analysis_candidate` | `id`; `cycle_id`; `manifest_id`; `execution_output_id`; `status`; structured facts/interpretations/support/counterevidence/confounders/unknowns/action_candidates；`revision`; timestamps | UQ execution output candidate type；strict payload Schema；manifest refs only | candidate mutable review state |
| `formal_analysis` | `id`; `cycle_id`; `candidate_id`; `manifest_id`; `execution_binding_id`; `version_no`; finalized fields；`confirmed_by/at`; `replaces_id?`; `stale_at/reason?`; `canonical_hash` | UQ cycle+version；candidate once；current non-stale determined query；same-cycle replacement | immutable; stale marker is separate dependency state or narrowly controlled column |
| `observation_action` | `id`; `cycle_id`; `action_type`; `reason`; `next_observation_point_id?`; `submitted_by/at`; `command_receipt_id` | action includes `CONTINUE_OBSERVING/ADD_EVIDENCE/END_INVALID`; never HumanDecision | immutable |
| `human_decision` | `id`; `cycle_id`; `formal_analysis_id`; `decision_type`; `reason`; `evidence_refs`; `expected_change`; `version_no`; `confirmed_by/at`; `replaces_id?`; `canonical_hash` | UQ cycle+version；only user actor；valid close uses current analysis/all validity；no CONTINUE | immutable |
| `iteration_plan` | `id`; `task_id`; `source_decision_id`; `action_type`; target/scope/reference/model/agent/candidate_count/budget/expected_change/release draft；`status`; `revision`; `confirmed_by/at?` | UQ decision+active plan；no plan for pause/end；bounded by baseline/policy | candidate then confirmed immutable version semantics |
| `iteration_plan_target` | `plan_id`; `target_type/id`; `change_scope`; `must_change`; `preserve_scope`; `ordinal` | composite PK；targets current task objects/package；scope schema | immutable after confirm |
| `cycle_comparison` | `id`; `task_id`; `preceding_cycle_id`; `following_cycle_id`; `deterministic_comparability`; `semantic_outcome`; support/counter/confounder/unknown refs；`manifest_hash`; `confirmed_by/at` | UQ ordered pair；following number=preceding+1 and both valid；D owns comparability | immutable |
| `cycle_time_reconciliation` | `id`; `cycle_id`; active minutes/components；method；baseline ref；`confirmed_by/at` | UQ cycle；minutes>=0；first due every ended V1.1+ cycle | immutable |
| `value_survey` | `id`; `task_id`; `preceding/following_cycle_id`; three ratings；following-cycle intent/status；`confirmed_by/at` | UQ adjacent valid pair；ratings 1..5；N+2 semantics not fixed Cycle3 | immutable |
| `value_assessment` | `id`; pair refs；computed status；time result；survey result；serious incident flag；method version；created_at | UQ pair+method；status `PASSED/UNCERTAIN/FAILED`; deterministic | immutable computed result |

### 2.10 `governance_ops` 配置、Prompt、审计、导出与删除

| 表 | 关键列 | 关键约束与索引 | 可变性/保留 |
|---|---|---|---|
| `config_bundle` | `id`; `config_type`; `scope`; `version_no`; `schema_version`; `payload`; `canonical_hash`; `status`; author/reviewer/time | UQ type+scope+version；strict Schema；CK type=`SCENE_TEMPLATE/AGENT_TEMPLATE/REVIEW_RULE/COMPLIANCE_POLICY/PLATFORM_RULE`；明确排除Prompt/provider/model/price及decision-AI配置 | immutable lifecycle metadata |
| `config_activation` | `id`; `config_type`; `scope`; `bundle_id`; `activation_revision`; `status`; `effective_at`; actor/reason | FK bundle且同一非Prompt closed type/scope；partial UQ one active per type/scope；monotonic revision；数据库CK/FK阻止`prompt_config_bundle`进入此表 | append/revoke/rollback；不是Prompt activation authority |
| `provider_profile` | `id/version`; provider code；endpoint region/data policy capability/error/timeout profile refs；secret ref name only；status | no secret values；UQ provider+version | immutable version |
| `model_profile` | `id/version`; provider profile；exact model/version；context/capabilities；allowed data；status | UQ provider+exact version/profile version | immutable |
| `price_version` | `id`; model profile；unit prices/currency/effective interval/source verified_at | no overlap for same price scope；amount>=0 | immutable temporal |
| `prompt_config_bundle` | `id`; `family_id`; `version_no`; `parent_id?`; normalized prompt/rule bytes ref+`content_hash`; exact provider/model/profile/adapter refs+hash；sampling/reasoning manifest ref+hash；renderer/context-builder/retrieval/chunker refs+hash；typed-variable-schema ref+hash；allowed-label/action-taxonomy refs+hash；context/output limits；tool/output/family-payload schema refs+hash；Review/compliance/data-policy/product version refs；`canonical_hash`; `config_lifecycle_status`; author/reviewer | UQ family+version/hash；canonical hash覆盖全部定义字段但不含secret；所有taxonomy/schema为封闭版本且`additionalProperties=false`；raw Prompt不得在生产自由编辑或公开返回；任一定义字段变化创建新ID/version/hash；config lifecycle闭合=`DRAFT/CANDIDATE/HUMAN_APPROVED/DEPRECATED`且不属于canonical hash，approve/deprecate只可用专用command receipt+audit做受控前向状态，不混入activation/evidence状态 | definition immutable；lifecycle metadata guarded，全部转移留receipt/audit |
| `evaluation_binding` | `id`; candidate prompt-config ref+hash；`comparison_mode`; `comparison_basis`; `control_kind`; control prompt-config或typed baseline ref+hash?；`change_set_ref/hash?`; blinded pair/order plan ref+hash?；gold/rubric/threshold/hard-fail-policy refs+hash；deterministic-validator ref+hash；`judge_prompt_config_ref/hash?`; judge-config/human-dataset refs+hash；exact candidate/control/judge model/profile refs+hash（适用时）；runtime/environment-fingerprint ref+hash；arm/role repeat-count、randomization/seed-policy与有界call plan；target/judge result-schema refs+hash；approved_by/at；`canonical_hash` | mode=`DIRECT/PAIRED`；DIRECT要求basis=`ABSOLUTE_ONLY`且control/change-set/pair-order为空。PAIRED basis=`PROMPT_ONLY/FACTORIAL/BASELINE_GATE`并要求匹配control ref/hash及盲化A/B顺序交换计划。`PROMPT_ONLY => control_kind=PROMPT_CONFIG`，两arm的provider/exact model/profile/adapter、sampling/reasoning、基础input/context/case必须相等且只允许change-set声明的Prompt factor不同。`BASELINE_GATE => control_kind=HUMAN_BASELINE|NO_AI_BASELINE`，只用于批准的cold-start baseline，不冒充Prompt A/B且不创建control provider TARGET lane。FACTORIAL必须在plan中封闭声明允许的`PROMPT_CONFIG|HUMAN_BASELINE|NO_AI_BASELINE` control kind、全部变化因子与有效组合，不得把结果归因单一Prompt；typed baseline始终不得创建provider TARGET lane。canonical hash覆盖mode/basis/control/change-set、两arm、blind/order与全部评测定义；使用LLM judge时judge身份须与arms分离，human-only禁止JUDGE call；任一字段变化建立新binding；不保存current status | immutable evidence definition |
| `evaluation_run` | `id`; evaluation_binding_id；`source_authorization_receipt_ref/hash?`; `assessment_revision`; `assessment_kind`; `evaluation_evidence_status`; `eligibility_status`; candidate/control config-or-baseline refs+hash；按arm/role的execution/model-call/artifact manifests refs+hash；actual candidate/control/judge model/profile refs+hash（适用时）；actual blinded order/swap manifest ref+hash；actual runtime/environment-fingerprint ref+hash；actual repeat/randomization/seed refs；actual deterministic-validator ref+hash；result-schema refs+hash；`run_status`; per-dimension results?；cost/latency?；raw artifact object ref/hash?；`trigger_ref`; `supersedes_id?`; `finalization_command_id/request_digest?`; `canonical_hash?`; started/completed/recorded_at | UQ binding+assessment revision/hash；kind=`RUN_RESULT/INVALIDATION/REQUALIFICATION`；RUN_RESULT/REQUALIFICATION必须引用typed authorization receipt，partial UQ one result-like assessment per source authorization；INVALIDATION要求trigger且authorization为空。run status闭合=`AUTHORIZED/RUNNING/FINALIZING/COMPLETED/FAILED`；授权创建时即生成稳定run id，resultRef指向它；只允许受控前向状态，COMPLETED/FAILED后不可变。finalizer锁run+binding，以稳定commandId/digest幂等；同key同digest重放同assessment，异digest冲突，并在一个事务分配单调revision、冻结完整actual evidence、blind/order、result/hash。实际定义必须逐项匹配binding：DIRECT只验candidate；PROMPT_ONLY验两个provider arm与order-swap；BASELINE_GATE验candidate artifact和typed baseline artifact/authority receipt且control model-call必须为空；FACTORIAL按冻结plan验组合。缺任一所需证据或泄露盲化身份均不得eligible，human-only禁止judge calls；只从最新COMPLETED有效revision投影current资格 | 一个run root有窄状态推进，终态行组成append-only eligibility assessment stream；partial artifacts留在对应ExecutionOutput并由run query投影；自动化最多产生OfflinePassed证据 |
| `prompt_activation` | `id`; environment；family_id；activation_scope；`model_profile_id`; prompt config/evaluation refs+hash；`eligibility_assessment_ref/hash/revision`; `required_comparison_mode/basis`; `required_control_ref/hash?`; `required_change_set_ref/hash`; activation_revision；lifecycle_status；`rollout_manifest_schema_version/ref/hash?`; `rollout_revision?`; effective_at/expiry?；activated/revoked reason | UQ revision；partial UQ one Active per`environment+family+scope+modelProfile`；PromptConfig exact model/profile必须匹配key；CK lifecycle=`EXPLICIT_PILOT/SHADOW/CONTROLLED_CANARY/ACTIVE/DEPRECATED/REVOKED/ROLLED_BACK`；only latest eligible assessment；绝无`UNVERIFIED`。Prompt变更默认要求assessment精确匹配当前verified LKG的PAIRED PROMPT_ONLY或获批FACTORIAL change-set；首版无LKG要求BASELINE_GATE；V1的DIRECT只提供绝对维度，不能单独晋升，且本合同不定义绕过comparison门的人工例外。PILOT/SHADOW/CANARY还必须冻结immutable rollout manifest：mode、完整activation key/config、task/execution allowlist、费用/容量、stop conditions、effective/expiry/revoke；晋升/撤销建新revision，不能回写旧manifest | append lifecycle；每模型独立champion/LKG/revoke/rollout authority proof |
| `command_receipt` | `id`; `command_id`; actor_id；command_type；target_type/id；idempotency_key_hash；request_digest；status；result_ref；result_summary；`result_manifest_schema_version/ref/hash?`; `authorization_kind?`; `authorization_schema_version?`; `authorization_manifest jsonb/object_ref?`; `authorization_canonical_hash?`; `authorization_event?`; `supersedes_receipt_id?`; cleanup_status?；created/expires_at | UQ `(actor_id,command_id)`；UQ `(actor,command_type,target_type,target_id,idempotency_key_hash)`；same scoped key diff digest conflict；若命令产生可重建的typed result，schema/ref/hash必须三者齐全并指向不可变stored object version/content hash，重放返回同一组值。`DELIVERY_GRANT`必须使用strict `delivery-grant-intent/v1` result manifest并冻结服务端预分配locator/ref/hash；authorization kind=`OFFLINE_EVALUATION/SHADOW_EVALUATION_CONSENT`且event=`AUTHORIZED/REVOKED`，strict manifest/ref与expires_at均入canonical hash，revoke以新receipt引用原授权；非授权命令authorization字段全空；business UQ outlives receipt | immutable；授权receipt及其revoke chain按评测证据保留，JIT从原授权+最新事件+expiry投影current authority；typed result manifest/hash不可回写；`cleanup_status`仅删除命令使用 |
| `activity_event` | `id bigserial/uuid`; `event_type`; `aggregate_type/id/revision`; actor；occurred_at；payload_summary；visibility | monotonic cursor index；no body；IDX task/occurred | durable SSE/activity history per retention |
| `audit_event` | `id`; actor/role；action；target type/id/revision；reason；request/trace/error refs；outcome；occurred_at；content_classification | append-only；no正文/Prompt/secret；IDX target/time/actor | non-content security/admin subset 180d |
| `export_request` | `id`; actor/task；export_type；source_manifest/hash；status；revision；timestamps | UQ semantic request/command；source immutable；IDX status；关联job由`durable_job.export_request_id`唯一反查，避免双向FK/双真相 | root |
| `export_artifact` | `id`; request_id；object_version_id；media_type/size/hash；manifest version；created_at/expires_at? | UQ request+format；object hash match | immutable, lifecycle per export policy |
| `deletion_request` | `id`; task_id；command_id；ledger_intent_ref/high_watermark；request_status；`cleanup_status`; requested_by/at；PG tombstoned/objects reconciled/completed timestamps | UQ task active deletion、command；ledger ref required before PG tombstone；cleanup=`PENDING/IN_PROGRESS/COMPLETE/FAILED_RETRYABLE` | state machine; no raw content |
| `deletion_progress` | `id`; deletion_request；target type/id/hash；stage；status；attempt/error；timestamps | UQ request+target+stage；IDX pending；closed stage至少含PG/OBJECT/DERIVED/DELIVERY_DISPOSITION/SECURE_ERASE/CLIENT_MARKER，未知stage拒绝 | append/state for reconciliation |
| `recovery_checkpoint` | `id`; checkpoint version/time；`cut_algorithm`; PG timeline/LSN/ref；checkpoint epoch或object-ref watermark；object manifest version/shard count/Merkle root/cursor；ledger high_watermark；`component_manifest_schema_version`; `component_manifest_ref/hash`; config-set ref/hash；schema version/ref/hash；compatible application artifact ref/hash；recovery procedure/runbook version/ref/hash；`checkpoint_hash?`; `status`; `signature_ref?`; `revision`; timestamps | UQ checkpoint version；partial UQ finalized checkpoint hash；CK status=`BUILDING/VERIFYING/RECOVERABLE/FAILED`；cut identity从创建起不可变；strict component manifest列出并覆盖PG cut、全部object shards/Merkle、ledger HWM、schema/config、兼容应用制品、恢复步骤与各自ref/hash/version；进入VERIFYING前固定全部component refs并纳入checkpoint hash，RECOVERABLE时全部字段非空且逐项通过signature/hash/coverage校验；只允许BUILDING→VERIFYING→RECOVERABLE或BUILDING/VERIFYING→FAILED | 受控状态root；RECOVERABLE/FAILED后全字段不可变，只有RECOVERABLE可开放restore gate |

Prompt定义与激活不混表：A05的PromptConfig `approve/deprecate`只推进`prompt_config_bundle.config_lifecycle_status`并写正式command receipt/audit，不改canonical定义；`pilot/shadow/canary/activate/revoke/rollback`只追加`prompt_activation` revision。二者都不能写通用`config_activation`；后者不能接收Prompt、decision family、model/provider或price bundle，也不能成为旁路。

Evaluation authorization不是普通receipt摘要。`evaluation-authorization/v1` manifest的`authorizationKind`精确使用`OFFLINE_EVALUATION|SHADOW_EVALUATION_CONSENT`，并至少冻结`candidatePromptConfigRef/hash,comparisonMode,comparisonBasis,controlKind/controlRef/hash,changeSetRef/hash,blindedPairOrderPlanRef/hash,evaluationBindingRef/hash,targetJudgePlanRef/hash,datasetManifestRef/hash,license/entitlement refs,policy/price refs,budgetCeiling/reservation/costOwner,expiresAt,allowedOutputOwner=EVALUATION_ARTIFACT_ONLY`。OFFLINE由管理员授权，明确`userSlot=N/A`且不可伪造用户同意。SHADOW授权receipt自身就是D01用户consent权威，不在manifest内反向引用自身；其canonical hash直接覆盖receipt的`actorId,commandId,requestDigest`、disclosure schema/ref/hash、`taskId,businessExecutionId,inputManifestRef/hash,incrementalCostDisclosure,userSlotReservationRef`，并单向引用`prompt_activation`中独立且不可变的`rolloutAuthorityRef/hash/revision`与rollout allowlist ref/hash。原授权receipt只记录AUTHORIZED，撤销用新REVOKED receipt引用它；JIT在锁内重算manifest/hash、检查rollout authority revision、expiry与最新事件，任何字段缺失、漂移、过期或撤销均fail closed。

`BASELINE_GATE`的HUMAN/NO_AI control不是虚构的provider lane。它必须由strict `typed-baseline-artifact/v1`（不可变stored object version+content hash）和独立人工批准command receipt共同定义，至少冻结baseline kind、适用family/model-profile key、case/input/rubric/schema、人工或确定性产出、来源/provenance、限制、批准人/职责分离和有效期。该receipt的typed result manifest ref/hash是CONTROL arm权威证据。BASELINE_GATE的JUDGE selector/JIT等待candidate TARGET artifact receipt与baseline authority/artifact receipt；finalizer把后者作为CONTROL arm evidence并验证order plan，但不得创建control ModelCall、provider usage或费用。PROMPT_ONLY仍要求两个真实provider TARGET arm；FACTORIAL按其冻结factor/control-kind plan判别，三者不得互换。

独立 deletion ledger 不放在可回退到旧 PG 时间线的同一权威存储。其最小 record：`ledgerSchemaVersion, commandId, taskIdHash/stableId, intentType, requestedAt, actorId, retentionClass, previousLedgerHash, recordHash, sequence/highWatermark`；不含正文、参考、评论、Prompt、对象 URL 或 secret。

`recovery_checkpoint` 的“不可变恢复点”从 `RECOVERABLE` 开始成立，不把构建中状态伪装成完成清单。构建期间只允许追加/冻结由同一 checkpoint epoch 或 watermark 边界覆盖的组件引用；任一分页gap、超窗、hash/Merkle、对象覆盖或ledger high-watermark校验失败只能进入 `FAILED`，不得回退字段后重试成同一版本，必须新建 checkpoint。

删除与在途结果相交时，不允许在“永不丢未收据结果”和“7天内删除用户派生数据”之间形成死锁。ledger intent 与 PG tombstone 均已耐久后，先阻断该task的新job/input/call-start和普通`DELIVERY_BUFFER_CREATE` grant，取消并fence相关WORK lease。删除屏障前已经`CALL_START_COMMITTED`而结果尚未buffer的调用，只可取得更高fencing的封闭`DELETION_DISPOSITION` lease与隔离buffer grant，把已有outcome耐久化并直接报告discard；不得调用provider、读原业务输入或生成第二结果。若最终没有本地payload，API-owned reconciliation只有在全部相关WORK/DISPOSITION lease和写grant均失效、固定index HWM完整扫描无record且无并发处置后，才能幂等写`NO_PAYLOAD_DISPOSITION` receipt并把call/job置`OUTCOME_UNKNOWN_NO_PAYLOAD`；该proof只说明本系统无可恢复payload，不说明provider未处理数据。屏障等待所有pre-barrier intent进入正常buffered+receipted、deletion-disposition buffered+receipted或上述no-payload proof终态，并等待两类写grant及专用lease收口，再捕获/复核最终HWM与无迟到entry。任一证明缺失时cleanup fail closed。处置receipt不伪造原WORK lease、不创建用户派生事实；已发生费用只保留批准的最小非内容元数据。payload receipt允许INT-009安全擦除，no-payload receipt不调用INT-009；只有所有分支闭合才能`cleanupStatus=COMPLETE`。

每次`POST /input-grants`签发`DELIVERY_BUFFER_CREATE|DELETION_DISPOSITION_BUFFER`之前，API必须先以现有`command_receipt`持久化一个typed `delivery-grant-intent/v1` result manifest；它冻结`job/context/callIntent/reportKey/reportEnvelopeHash/resultHash`、预分配的record/payload locator ref+hash、grant purpose、deletion proof（适用时）、maxBytes和expiry，但不保存可用secret。payload、record或index写入任一阶段崩溃时，该receipt仍是孤儿扫描的权威输入。`NO_PAYLOAD_DISPOSITION` proof必须逐项引用该call所有grant-intent receipt，并证明每个预分配locator从未可见或已完成可验证secure erase，再结合固定index HWM无record；仅凭unreceipted index未命中不得宣称无payload。DeliveryStore若提供原子不可见commit，也必须以合同测试证明payload/envelope/record/index在commit前对业务与cleanup均不可见、失败可按grant intent完整回收。

## 3. 跨表硬约束与事务

### 3.1 必须由数据库和 D2 双重守住

1. 每 task 最多一个 active Cycle：partial unique index + task row lock。
2. Cycle number 在 task lock 内取 `next_cycle_number` 并永久递增；失败事务不消耗或复用是否允许需在 DDL 冻结，但已提交编号绝不重排。
3. ActualRelease 与 Cycle 创建、观察点、receipt、activity/audit 和 task projection 同事务。
4. user paid slot 与 task business slot 使用 partial unique；Redis lock 不参与正确性。
5. 同一 idempotency key/digest 并发只产生一个 receipt/业务结果；key重用不同digest为409。
6. Candidate formalize once；正式版本、snapshot、feedback、analysis、decision、config/evaluation/binding/output/cost 不覆盖。
7. replacement/correction 的 predecessor、replacement 与 task/cycle/aggregate 必须一致，链不能形成环。
8. execution binding 在 provider call 前存在且不可变；结果/费用只追加到 attempt/call/output/ledger。
9. Worker result fencing token 必须等于 job 当前有效 lease；过期 token 只能记录拒绝审计，不能生成 candidate。
10. 删除只有 independent ledger intent durable 后才可 PG tombstone；restore只有ledger high-watermark可验证才开放。

### 3.2 推荐事务边界

- 普通草稿 save：单聚合 revision update + draft revision insert；不含外部调用。
- formal content command：锁 object/task → D2 → insert FormalVersion/Snapshot/items/MemoryChangeSet/receipt/audit/event → commit。
- execution authorize：锁 user/task slots → D2 → 按1..N模型lane原子insert一个request、每lane独立binding/initial attempt/job与逐lanecost reserve，再insert共享slot/批次总预算receipt/event → commit；任一lane建链失败则整批不授权。EVALUATION的JUDGE binding只冻结经批准的TARGET依赖选择器；JUDGE job在所需TARGET receipt齐全前保持不可claim，实际artifact ref/hash由JIT写入ModelCall的resolved-call-input manifest。
- report accept：锁job/typed owner → fencing+Schema+context+reportKey/requestDigest验证；progress、result、pure/artifact failure均写最小`job_report_receipt`。BUSINESS AI只在后验Schema/validator通过时insert execution output/cost/semantic candidate/event；EVALUATION TARGET/JUDGE只insert evaluation artifact/cost/run progress，另由API finalizer事务在完整plan、hard-fail与必要人审闭合后追加RUN_RESULT assessment；document/export/maintenance分别写各自owner result/progress。删除交叉路径只insert最小成本/审计、`DISCARDED_BY_DELETION`和deletion progress；均不混写其他分支owner。
- actual release command：见2.8，全部一次提交。
- formal analysis/decision：分别独立用户命令；不能在AI完成时自动一起写。
- config activation：锁 activation key → 验证assessment的candidate/config/model、required comparison mode/basis、LKG或cold-start control、change-set、两arm/换位/盲化与human approval；DIRECT一律不得单独晋升 → revoke previous/insert active/receipt/audit → commit。

事务内禁止模型/HTTP/ObjectStore传输、文件解析、长回填、等待用户或无界批处理。

### 3.3 索引与查询纪律

- 所有 FK 有支撑索引；所有 task 列表以 `(owner_account_id, updated_at DESC, id)` keyset。
- activity/audit/job/cost 使用时间+稳定ID游标；offset只允许小型静态管理列表。
- `lower(login_name)`不依赖locale推测，应用明确normalization并UQ；不启用citext扩展除非另批。
- 章节全文/参考结构检索先用普通结构列、必要时批准PG全文；不创建vector。
- JSONB GIN、全文、partial/covering index 只有绑定实际query plan/数据量/写放大证据后加入。
- 大表分区触发于已测维护/查询/retention压力，不因表名是event/cost就预建。

### 3.4 Cross-store consistent-cut 候选

ADR-0018接受前不得声称“PG最近备份+对象最近备份”构成一致恢复点。物理实现必须在下列两种 **Proposed** 算法中由decision owner明确选择且完成恢复演练，不能在实现中静默混用：

1. **Checkpoint epoch + PostgreSQL MVCC cut**：在短事务中冻结checkpoint epoch、PG timeline/LSN和该MVCC视图可见的正式`object_reference`集合；manifest物化采用有界快照/分片，不持有无界长事务。每个分片不可变并带hash，顶层记录分片集合/Merkle root和独立deletion-ledger high-watermark。
2. **Monotonic object-reference watermark**：每个正式object-reference在同一PG事务获得单调commit watermark；checkpoint选择watermark `W`，只接受覆盖`<=W`且仍属恢复集合的不可变分片manifest/Merkle root，并绑定PG timeline/LSN及独立ledger high-watermark。

两者都必须证明：对象version/hash先于正式引用存在；cut之后新增引用不被错误纳入；cut之后删除由ledger重放防复活；manifest分片缺失、Merkle/hash不符、PG cut或当前ledger high-watermark不可证时正式恢复门fail closed。epoch/watermark类型、分页大小、签名、checkpoint频率与存储位置仍为Unknown。

## 4. 公共 REST 合同

### 4.1 通用协议

- Base path：`/api/v1`；HTTPS；UTF-8 JSON；时间为 RFC 3339 UTC instant，另有IANA timezone字段。
- session cookie认证；状态变更附 `X-CSRF-Token`；不把token放URL/localStorage。
- `X-Request-Id` 可由可信client提供合法格式，否则服务端生成；响应总回显服务端requestId。
- 正式 command 必须有 `Idempotency-Key` header；body仍带 `commandId` 供跨系统/ledger稳定引用。
- `If-Match` 可用于普通资源ETag；正式命令以body `expectedRevision`为唯一清晰口径。是否同时要求header由API ADR冻结，不允许双值不一致。
- 正文/Prompt/raw output、对象URL、secret不进入查询列表、错误或SSE。

### 4.2 查询响应 envelope

```json
{
  "schemaVersion": "flowverse.api.response/v1",
  "data": {},
  "meta": {
    "requestId": "uuid",
    "serverTime": "2026-08-14T00:00:00Z",
    "resourceRevision": 12,
    "capabilities": [],
    "nextAction": null,
    "degradationMode": "NORMAL",
    "affectedCapabilities": [],
    "dataFreshness": "CURRENT",
    "asOf": "2026-08-14T00:00:00Z",
    "lastKnownGoodRef": null,
    "retryable": false,
    "retryAfter": null
  }
}
```

`capabilities[]` 至少：`actionId, enabled, reasonCodes[], severity, resolutionRoute?, expectedRevision, impactPreviewRef?`。`nextAction` 最多一个 primary；语义模型建议不直接放成 mutation action。

`degradationMode/affectedCapabilities/dataFreshness/asOf/lastKnownGoodRef/retryable/retryAfter`是所有query、receipt和error的共通恢复字段，枚举与UIUX合同一致。`dataFreshness`候选闭合集为`CURRENT/STALE/VERIFIED_LAST_KNOWN_GOOD/UNKNOWN`；只有`CURRENT`可来自满足该资源权威新鲜度的PG路径，缓存/只读副本/客户端副本不得冒充current。非current必须给权威`asOf`（确实不可知时null），`VERIFIED_LAST_KNOWN_GOOD`还必须给可授权解析的`lastKnownGoodRef`；所有formal、release、decision、AI和对象finalize capability fail closed，已授权历史可在明确标识下只读。JSON `retryAfter`若存在统一为RFC 3339 UTC最早重试时刻；HTTP `Retry-After`可按标准使用秒数或日期，但两者不得矛盾。

集合 `meta.page`：`nextCursor?`, `hasMore`, `limit`; cursor是opaque且绑定sort/filter/actor，不暴露SQL offset。默认limit/最大limit需按payload和性能批准。

### 4.3 正式命令 request/receipt

```json
{
  "schemaVersion": "flowverse.command/v1",
  "commandId": "uuid",
  "targetRef": {"type": "TASK", "id": "uuid"},
  "expectedRevision": 12,
  "payload": {},
  "presentationCapabilityRef": {
    "id": "opaque-short-lived-id",
    "revision": 4
  },
  "clientContext": {
    "occurredAt": "2026-08-14T00:00:00Z",
    "routeId": "P02",
    "locale": "zh-CN"
  }
}
```

`presentationCapabilityRef` 是官方 Web renderer 根据自己测得的当前 session/route/layout mode 换取的短时、服务端签名引用。它只用于官方 Web 的UX一致性和防止resize/route/revision后的陈旧提交：缺失、过期、route/actor/revision不符或mode=`READ_ONLY`时，官方Web受限命令返回`PRESENTATION_CAPABILITY_REQUIRED/MOBILE_COMPLEX_ACTION_DISABLED`。它不是身份、角色、设备证明或业务授权；query参数、User-Agent和该签名都不能证明物理viewport，非官方客户端可以声明desktop mode，因此不得把它作为恶意客户端防绕过边界。D2始终独立重验actor/ownership/policy/target revision和全部业务安全条件。若未来要求在所有客户端强制设备/viewport限制，必须另行批准managed-client/device-attestation合同；当前不伪造这种能力。layout跨767/768、1279/1280后官方Web必须刷新引用，旧引用不可用于受限命令。

成功同步或异步均返回：

```json
{
  "schemaVersion": "flowverse.command-receipt/v1",
  "receipt": {
    "receiptId": "uuid",
    "commandId": "uuid",
    "status": "COMPLETED",
    "targetRef": {"type": "TASK", "id": "uuid"},
    "resultRefs": [],
    "newRevision": 13,
    "nextAction": null,
    "acceptedAt": "2026-08-14T00:00:00Z"
  },
  "meta": {"requestId": "uuid", "serverTime": "2026-08-14T00:00:00Z", "degradationMode": "NORMAL", "affectedCapabilities": [], "dataFreshness": "CURRENT", "asOf": "2026-08-14T00:00:00Z", "lastKnownGoodRef": null, "retryable": false, "retryAfter": null}
}
```

删除命令的 receipt 额外返回 `cleanupStatus=PENDING|IN_PROGRESS|COMPLETE|FAILED_RETRYABLE`；其他命令省略该字段。`COMPLETED` 表示 ledger intent 与 PG 不可访问 tombstone/ledger cursor 已耐久，不等于物理清理完成。`cleanupStatus=COMPLETE` 还要求相关 DeliveryStore 记录已经正常生命周期清理，或取得 `DISCARDED_BY_DELETION` receipt 并完成可验证安全擦除。`GET /tasks/{taskId}/deletion` 返回 `requestStatus`、`cleanupStatus`、已完成/待处理阶段、最近安全错误类别与更新时间，不返回正文、对象 locator 或 ledger secret。

异步受理用 `202 Accepted` + status `ACCEPTED/QUEUED`；创建普通资源可 `201`; 已完成command通常 `200`。相同key同digest返回相同业务receipt，不因重复请求换新ID。

### 4.4 错误 envelope 与语义

```json
{
  "schemaVersion": "flowverse.error/v1",
  "error": {
    "code": "REVISION_CONFLICT",
    "errorId": "uuid",
    "message": "内容已发生变化，请重新审阅。",
    "targetRef": {"type": "CONTENT", "id": "uuid"},
    "preserved": true,
    "currentRevision": 14,
    "details": [{"field": null, "reasonCode": "STALE_PREVIEW"}],
    "recoveryActions": [{"actionId": "RELOAD_AND_COMPARE", "route": "/..."}]
  },
  "meta": {"requestId": "uuid", "serverTime": "2026-08-14T00:00:00Z", "degradationMode": "PARTIAL", "affectedCapabilities": ["FORMAL_WRITE"], "dataFreshness": "UNKNOWN", "asOf": null, "lastKnownGoodRef": null, "retryable": false, "retryAfter": null}
}
```

| HTTP | 稳定语义 | 典型 code |
|---|---|---|
| 400 | malformed/invalid protocol | `INVALID_REQUEST/INVALID_CURSOR` |
| 401 | 无/过期session或需改密 | `AUTH_REQUIRED/SESSION_EXPIRED/PASSWORD_CHANGE_REQUIRED` |
| 403 | 已认证但角色/capability禁止 | `FORBIDDEN/ADMIN_CANNOT_CONFIRM/MOBILE_COMPLEX_ACTION_DISABLED` |
| 404 | 不存在或为防枚举隐藏的越权对象 | `RESOURCE_NOT_FOUND` |
| 409 | revision、幂等digest、状态/业务唯一冲突 | `REVISION_CONFLICT/IDEMPOTENCY_KEY_REUSED/ACTIVE_CYCLE_EXISTS` |
| 413 | 当前生效配置允许的大小上限 | `PAYLOAD_TOO_LARGE/OBJECT_TOO_LARGE` |
| 422 | JSON Schema/业务字段校验 | `VALIDATION_FAILED/UNKNOWN_ENUM` |
| 429 | 已批准限流/资源配额 | `RATE_LIMITED/USER_PAID_SLOT_BUSY/QUEUE_CAPACITY_REACHED` |
| 503 | 必需依赖/quorum/能力暂不可用 | `WRITER_UNAVAILABLE/AI_CAPABILITY_UNAVAILABLE/OBJECTSTORE_UNAVAILABLE` |

精确使用423等扩展status需另批；客户端主要按稳定`code`，未知code走安全通用错误并保留输入。

只有服务端将失败分类为transient、返回`retryable=true`，且该GET endpoint的自动重试metadata与次数/总时长预算均已批准时，才可由一个明确owner执行有界退避+jitter；429/503若给出`Retry-After`必须服从。预算/metadata未冻结、没有权威响应的transport failure或缺少`Retry-After`且无批准fallback时，默认只提供手动安全恢复，不由客户端猜测上限。正式command、付费AI、object finalize、release/decision和unknown outcome不得自动新建key重试：先按同一`commandId`/receipt查询，相同idempotency key+digest的安全重发仍受批准总时长限制。401/403/404/409/422及确定性失败不自动重试。

### 4.5 独立 operational router allowlist

Operational health 不是业务 Public API，也不计入第5节 `PUB-001..PUB-107`。production H0 只允许下列封闭集合；新增 method/path、扩大暴露面或把它用于业务 capability/readiness 都必须另行批准：

| ID | Service/method/path | 暴露与身份 | 固定语义 |
|---|---|---|---|
| `OPS-API-001` | API `GET /health/live` | 仅批准的 LB/orchestrator/ops 探针；不得进入产品导航 | 只证明进程可响应；不调用 PG、Worker、ObjectStore、Redis 或 provider |
| `OPS-API-002` | API `GET /health/ready` | 仅批准的 LB/orchestrator/ops 探针；由受控 listener/probe audience 服务器侧固定 `PUBLIC` 或 `INTERNAL` scope，客户端 query/header不能自行扩权 | 响应显式带scope；PUBLIC只看writer/schema/public pool与接流条件，INTERNAL另看workload identity/claim-result schema/internal pool与预算；两者不混成一个布尔、不互相级联摘流，且均不得调用 Worker或代表任一业务 capability 可用 |
| `OPS-API-003` | API `GET /health/dependencies` | 私网或受认证运维面，不经 public product Edge | 展示有界、脱敏的 API-owned 依赖诊断；不得聚合 Worker 业务状态、正文、对象 locator 或 secret |
| `OPS-WORKER-001` | Worker `GET /health/live` | 私网 workload/ops 网络 | 只证明 Worker 进程可响应；不探测业务 PG |
| `OPS-WORKER-002` | Worker `GET /health/ready` | 私网 workload/ops 网络 | 只证明 registration/config/DeliveryStore 与接收获批 workload 的本地条件；production Worker 无业务 PG credential，不能直接探测业务 PG |

现有非业务诊断三件套必须作为一个 profile 管理：Web Check page、API `GET /api/v1/system/chain`、Worker `GET /internal/v1/system/status` 仅能在 ADR-0005 明确隔离的非生产 diagnostic profile **同时**启用。production H0 必须从产品 Web build/router 移除或隔离 Check page，并对后两条 route 不注册或返回 `404/410`；同时用依赖图证明 API 不调用 Worker。上述 `OPS-*` 路由独立保留，不得借诊断 profile 进入产品导航或反向形成 API→Worker 调用。

## 5. Public endpoint catalog

以下是完整**业务**资源/命令目录候选；`Q`=query，`D`=普通draft mutation，`C`=正式/有副作用command。`First`表示首次到期版本，不授权当前实现；operational health 只取第4.5节封闭集合。

### 5.1 会话、Shell、能力与收据

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| C | `POST /auth/login` | 建立session；统一失败响应；可能返回must-change capability | V1.0 |
| Q | `GET /auth/session` | 当前actor/role/expiry/csrf metadata/capabilities | V1.0 |
| C | `POST /auth/password-change` | 首次/主动改密并轮换session | V1.0 |
| C | `POST /auth/logout` | 服务端撤销session | V1.0 |
| Q | `GET /work-home` | Bot/continue/pending/task-list独立section envelope | V1.0 |
| Q | `GET /capabilities?routeId=&taskId=&presentationMode=` | route/action capability与唯一next action；`presentationMode`是不可信UX hint，官方renderer据此换取短时ref用于陈旧提交防护，不构成viewport证明 | V1.0 |
| Q | `GET /command-receipts/{receiptId}` | 网络结果未知时取权威命令结果 | V1.0 |
| Q | `GET /command-receipts/by-command/{commandId}` | 响应丢失时用客户端已知commandId按当前actor授权定位同一receipt；不把Idempotency-Key放URL | V1.0 |
| Q | `GET /activity-events?taskId=&cursor=` | 可分页活动历史 | V1.0 |
| Q | `GET /events?taskId=&cursor=` | SSE，详见第6节 | V1.0 |

Bot 最小合同：

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| Q/C | `GET/POST /bot/conversations` | 获取global/task scope会话或显式创建；不自动改变当前task | V1.0 |
| Q | `GET /bot/conversations/{id}/messages?cursor=` | message、action card、未应用draft分页历史；上下文revision可见 | V1.0 |
| C | `POST /bot/conversations/{id}/messages` | 以clientMessageId幂等创建用户消息和候选响应execution；占用适用付费槽 | V1.0 |
| Q | `GET /bot/action-cards/{id}` | 导航descriptor、target、context revision、expiry与失效原因 | V1.0 |
| C | `POST /bot/unapplied-drafts/{id}/commands/prepare-application` | 只生成owning page的可编辑表单草稿/导航，不写正式对象 | V1.0 |
| C | `POST /bot/unapplied-drafts/{id}/commands/discard` | 用户显式丢弃候选草稿，保留最小审计 | V1.0 |

Bot action card 只能导航 owning page，永不直接执行 mutation；message/draft 的 scope、context revision、expiry、execution/slot linkage均由服务端返回并在使用时重验。Bot区加载/执行失败不影响work-home其他section和确定性task入口。

### 5.2 Task 与双基线

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| Q/C | `GET/POST /tasks` | 列表/创建新小说task；POST有idempotency但不确认baseline | V1.0 |
| Q/D | `GET/PATCH /tasks/{taskId}` | cockpit view / 修改允许的普通字段expectedRevision | V1.0 |
| Q/D | `GET/PUT /tasks/{taskId}/stage0-drafts/creation` | CreationBaseline draft | V1.0 |
| C | `POST /tasks/{taskId}/commands/confirm-creation-baseline` | 人类确认不可变version | V1.0 |
| Q | `GET /tasks/{taskId}/creation-baselines` / `{versionId}` | 版本/impact | V1.0 |
| Q/D | `GET/PUT /tasks/{taskId}/stage0-drafts/operation` | OperationBaseline draft | V1.1 |
| C | `POST /tasks/{taskId}/commands/confirm-operation-baseline` | 人类确认/替换；传播影响 | V1.1 |
| Q | `GET /tasks/{taskId}/operation-baselines` / `{versionId}` | 版本/impact | V1.1 |
| Q | `GET /tasks/{taskId}/execution-preferences` / `{versionId}` | 高级设置的当前/历史未来默认偏好及所绑定CreationBaseline | V1.0 |
| C | `POST /tasks/{taskId}/execution-preferences` | 创建边界内不可变偏好version；越界要求替换baseline | V1.0 |
| C | `POST /tasks/{taskId}/commands/pause`、`.../resume`、`.../terminate`、`.../archive`、`.../restore-archive` | D10五个显式命令；移动全部禁用 | V1.0按到期mode |
| C | `POST /tasks/{taskId}/commands/request-deletion` | ledger-first task删除 | V1.0 |
| Q | `GET /tasks/{taskId}/deletion` | 删除进度/不可访问状态，不返回正文 | V1.0 |

不使用 `DELETE /tasks/{id}` 表示立即物理清除，因为用户动作需要intent、状态、异步清理、防复活和receipt。

### 5.3 参考与对象上传

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| C | `POST /tasks/{taskId}/reference-upload-sessions` | 创建logical object/quarantine upload grant | V1.0 |
| C | `POST /reference-upload-sessions/{sessionId}/commands/finalize` | 封存session并创建verification job | V1.0 |
| Q | `GET /tasks/{taskId}/references` / `/references/{id}` | metadata/processing/rights/impact | V1.0 |
| D | `PATCH /references/{id}` | rights/source/allowed usage expectedRevision | V1.0 |
| Q | `GET /references/{id}/extractions` / `/fragments?cursor=` | 提取状态和片段 | V1.0 |
| C | `POST /references/{id}/commands/confirm-partial-use` | 人类确认partial范围 | V1.0 |
| C | `POST /execution-previews/{id}/reference-selections` | 固定本次最小片段；不改全局权利 | V1.0 |
| C | `POST /references/{id}/commands/remove` | 影响预览后移除/删除 | V1.0 |
| C/Q | `POST /stored-objects/{id}/download-grants`; `GET /stored-objects/{id}/metadata` | 授权短时下载/metadata；仅有权限且状态允许 | V1.0 |

浏览器不得自行构造bucket/key；upload/download grant响应标`Cache-Control: no-store`，过期不自动扩大。对象 action×state 固定为：`VERIFIED` 仅允许受控 Worker 解析；`PROCESSING/PARTIAL` 不允许下载或进入任何 execution/snapshot/export manifest；只有 `COMMITTED` 可按 actor/owner/purpose 权限下载并进入 manifest；`UPLOADING/QUARANTINED/VERIFYING/REJECTED/DELETING/DELETED` 全部拒绝。

### 5.4 创作、候选、Review、正式版本与记忆

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| Q/C | `GET/POST /tasks/{taskId}/creative-objects` | 列出/建立允许类型对象 | V1.0 |
| Q | `GET /creative-objects/{id}` | metadata/current formal/draft/capabilities | V1.0 |
| D | `PUT /creative-objects/{id}/draft` | 保存章节级普通草稿；expectedRevision | V1.0 |
| Q | `GET /creative-objects/{id}/draft-history?cursor=` | 恢复/比较 | V1.0 |
| Q/C | `GET/POST /creative-objects/{id}/candidates` | 列表/人工编辑candidate；AI candidate由result内部产生 | V1.0 |
| D | `PATCH /candidates/{id}` | 人工编辑/状态；保留source/output linkage | V1.0 |
| C | `POST /candidate-sets/{setId}/commands/select-primary` | 选择主候选但不formal | V1.0 |
| Q/C | `GET/POST /candidates/{id}/review-runs` | 查询/触发当前有效配置允许的 Review | V1.0 |
| C | `POST /review-findings/{id}/commands/resolve` | 用户修复/非block风险接受/额外Review | V1.0 |
| Q | `GET /targets/{type}/{id}/unified-review` | 聚合read model，不覆盖来源 | V1.0 |
| Q | `GET /targets/{type}/{id}/semantic-candidates?cursor=` / `/semantic-candidates/{candidateId}` | owning target上的validated candidate、证据locator、冲突/缺口、stale/invalid状态 | family首次到期 |
| C | `POST /semantic-candidates/{id}/commands/accept-for-d2` | 人类接受当前candidate进入owning正式表单；不直接formal | family首次到期 |
| C | `POST /semantic-candidates/{id}/commands/edit-for-d2` | 保存显式人工编辑review outcome；原candidate不覆盖 | family首次到期 |
| C | `POST /semantic-candidates/{id}/commands/reject` | 拒绝候选并保留原因 | family首次到期 |
| C | `POST /semantic-candidates/{id}/commands/request-evidence` | 请求补证据；候选保持非正式/可能stale | family首次到期 |
| C | `POST /candidates/{id}/commands/formalize` | D02；原子FormalVersion+Snapshot+MemoryChangeSet | V1.0 |
| Q | `GET /creative-objects/{id}/formal-versions` / `{versionId}` | 正式版本与正文按需 | V1.0 |
| Q | `GET /tasks/{taskId}/content-snapshots` / `{snapshotId}` | snapshot manifest/compare/releasability | V1.0 |
| Q/C | `GET /memory-change-sets/{id}`; `POST .../commands/confirm` | 人审记忆变化并形成MemoryVersion | V1.0 |
| Q | `GET /tasks/{taskId}/work-memory` / `/work-memory-versions/{id}` | 当前/历史记忆 | V1.0 |

### 5.5 AI执行、队列、费用与只读轨迹

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| C | `POST /tasks/{taskId}/execution-previews` | D层组装预览；不调用模型 | V1.0 |
| Q | `GET /execution-previews/{id}` | 模型/角色/输入/参考/费用/阻断/expiry | V1.0 |
| C | `POST /execution-previews/{id}/commands/authorize` | D01；原子生成BUSINESS request及逐lane binding/attempt/job/slot。若preview显式披露并由用户勾选Shadow的额外模型、输入数据范围、增量费用/上限、无业务写与停止条件，则同事务另签`SHADOW_EVALUATION_CONSENT` receipt并创建独立EVALUATION request/pool；未同意不得静默Shadow | V1.0 |
| Q | `GET /executions/{id}` | execution状态、partial、next action | V1.0 |
| Q | `GET /executions/{id}/attempts` / `/trace` / `/costs` | 只读拓扑、attempt、费用ledger | V1.0 |
| C | `POST /executions/{id}/commands/cancel` | 排队可取消；运行按安全取消点 | V1.0 |
| C | `POST /executions/{id}/commands/create-retry-preview` | 必须提交sourceLaneNo、replacesAttemptId和RETRY/FALLBACK kind；服务端验证attempt属于该execution/lane后创建只含原lane的新preview，不自动重试/跨lane换模 | V1.0 |
| C | `POST /executions/{id}/commands/resolve-unknown-outcome` | 人工恢复路径候选；具体动作受D层限制 | V1.0 |

V1.0只允许初始小说/Review workload；V1.1增加包装Review/分析；V1.2增加decision-driven plan/change/comparison。无通用`execute-anything` endpoint。

### 5.6 包装、投放与Cycle

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| Q/C | `GET/POST /tasks/{taskId}/packaging-candidates`; `GET /tasks/{taskId}/packaging-versions`; `GET /packaging-versions/{versionId}` | 人工候选或另行批准内容生成结果；正式版本列表标记current，by-id返回replacement chain与绑定snapshot，支持P04刷新/深链重建candidate/formal区分 | V1.1 |
| D/C | `PATCH /packaging-candidates/{id}`; `POST .../commands/formalize` | 编辑/确认PackagingVersion | V1.1 |
| Q/C | `GET/POST /tasks/{taskId}/release-plans` | draft/创建计划 | V1.1 |
| D/C | `PATCH /release-plans/{id}`; `POST .../commands/confirm` | 计划编辑/确认ready | V1.1 |
| C | `POST /release-plans/{id}/commands/confirm-actual-release` | 原子ActualRelease+Cycle | V1.1 |
| Q | `GET /tasks/{taskId}/cycles` / `/cycles/{id}` | Cycle、validity、观察点、next action；by-id内嵌当前coordination-time reconciliation状态/版本/是否到期，D12写后可重载 | V1.1 |
| Q | `GET /actual-releases/{id}` / `/release-evidence` | 外部事实/人类证据 | V1.1 |
| C | `POST /cycles/{id}/external-events` | 用户确认外部事件/差异；不自动抓取 | V1.1 |
| C | `POST /external-events/{id}/commands/correct` | 新更正记录和确定性传播 | V1.1 |

### 5.7 反馈、分析、决定、下一轮与价值

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| Q/D | `GET/PUT /cycles/{id}/feedback-draft` | 五态指标、评论草稿；保存不等于可入模 | V1.1 |
| C | `POST /cycles/{id}/commands/confirm-feedback-snapshot` | 人审/privacy/model use后冻结 | V1.1 |
| Q | `GET /cycles/{id}/feedback-snapshots` / `{snapshotId}` | 版本/更正链 | V1.1 |
| C | `POST /feedback-snapshots/{id}/commands/correct` | 新snapshot；旧依赖stale | V1.1 |
| C/Q | `POST /cycles/{id}/analysis-input-manifests`; `GET /analysis-input-manifests/{id}` | D层冻结分析输入/查看允许范围 | V1.1 |
| Q | `GET /cycles/{id}/analysis-candidates` / `{id}`; `GET /cycles/{id}/formal-analyses`; `GET /formal-analyses/{analysisId}` | 候选facts/解释/反证/干扰/未知；正式列表标记current，by-id返回source candidate/input snapshot/replacement chain，支持P05刷新/深链重建candidate/formal区分 | V1.1 |
| C | `POST /analysis-candidates/{id}/commands/formalize` | 用户确认正式分析 | V1.1 |
| C | `POST /cycles/{id}/observation-actions` | continue observing/add evidence/end invalid；非HumanDecision | V1.1 |
| C | `POST /cycles/{id}/human-decisions` | 当前正式分析后的用户决定 | V1.1 |
| Q | `GET /cycles/{id}/human-decisions` / `{id}` | 决定/替代链 | V1.1 |
| Q/C | `GET/POST /human-decisions/{id}/iteration-plans` | V1.2方案candidate/人工编辑 | V1.2 |
| C | `POST /iteration-plans/{id}/commands/confirm` | 确认scope/model/budget/expected/release draft | V1.2 |
| Q | `GET /tasks/{taskId}/cycle-comparisons/{precedingId}/{followingId}` | D comparability + S支持候选 | V1.2 |
| C | `POST /cycles/{id}/commands/reconcile-coordination-time` | 每个ended Cycle，V1.1首次到期；移动禁用 | V1.1 |
| C | `POST /tasks/{taskId}/value-surveys` | 首个有效对两轮问卷；simple mobile例外 | V1.2 |
| Q | `GET /tasks/{taskId}/value-assessments/{pairId}` | deterministic个人价值，不等市场验证 | V1.2 |

### 5.8 导出、数据控制与管理员

| Kind | Method/path | 用途 | First |
|---|---|---|---|
| C/Q | `POST /tasks/{taskId}/exports`; `GET /exports/{id}` | 不可变manifest导出/状态 | V1.0按包类型 |
| C | `POST /exports/{id}/download-grants` | 已生成授权下载；D11移动窄例外 | V1.0 |
| Q/C | `GET/POST /admin/accounts`; `PATCH /admin/accounts/{id}` | 预置账号管理、锁/禁用；不创建用户正式session | V1.0 |
| Q | `GET /admin/config-bundles?type=` / `/{id}` | 只读版本registry/diff | V1.0 |
| C | `POST /admin/config-bundles` | 受控提交候选，不直接Active | V1.0 |
| Q/C | `GET/POST /admin/evaluation-runs`、`POST /admin/evaluation-runs/{id}/commands/revoke-authorization` | POST只创建`OFFLINE_EVALUATION`授权：以管理员评测权限冻结candidate、comparison mode/basis、control/change-set/blind-order、arm×role有界plan、dataset/license/policy/price/budget/expiry与artifact-only owner，形成immutable authorization receipt、稳定run ID和EVALUATION preview；不占用户business slot。执行共用AI job/JIT/DeliveryStore但禁止business candidate/formal；单结果仅写artifact/progress，finalizer在全部plan、basis/hard-fail/人审闭合时幂等追加唯一RUN_RESULT。revoke追加receipt事件；GET查询授权链、run进度、证据和分歧；自动最多OfflinePassed | V1.0 AI前 |
| Q | `GET /admin/prompt-activations` | 当前activation/LKG/evidence状态 | V1.0 AI前 |
| C | `POST /admin/prompt-configs/{configId}/commands/approve`、`.../deprecate` | 只推进PromptConfig专用lifecycle metadata并写receipt/audit，绝不写activation；author不能自批。若仍被active revision引用，deprecate必须拒绝，或与相应revoke/rollback通过同事务/outbox对账闭合后才成功 | V1.0 AI前 |
| C | `POST /admin/prompt-activations/{familyId}/commands/start-pilot`、`.../start-shadow` | body必须含environment+scope+modelProfileId+expectedRevision及strict rollout manifest ref/hash，以完整key开启独立可见试点/Shadow配置状态；manifest冻结mode、candidate config、task/execution allowlist、费用/容量、stop conditions、effective/expiry，receipt/resultRef指向新activation revision。start-shadow不等于某次用户调用同意，每次真实Shadow还必须引用D01签发的`SHADOW_EVALUATION_CONSENT` receipt并逐项匹配rollout authority revision、task/execution/input scope、增量费用/slot和allowlist | V1.0 AI前 |
| C | `POST /admin/prompt-activations/{familyId}/commands/promote-canary`、`.../promote-active` | 按完整family/scope/modelProfile key逐态晋升，必须引用匹配candidate/config/model及当前LKG或cold-start baseline的合格comparison assessment、change-set、人类批准和impact preview；DIRECT一律不能单独满足晋升 | V1.0 AI前 |
| C | `POST /admin/prompt-activations/{familyId}/commands/deprecate`、`.../revoke`、`.../rollback` | 按完整key逐态退出；只回退该modelProfile的verified LKG，无LKG时该lane AI不可选并回人工/确定性路径 | V1.0 AI前 |
| Q/C | `GET/POST /admin/model-profiles`; `/price-versions`; `/provider-policies`; `/platform-rules` | 版本候选/核验，不回显secret | 各首次使用前 |
| Q | `GET /admin/executions` / `/jobs` / `/capability-health` | 监控；管理员可终止执行但不改业务事实 | V1.0 |
| C | `POST /admin/executions/{id}/commands/terminate` | 运维终止；保留partial/cost | V1.0 |
| Q | `GET /admin/audit-events?cursor=` | 最小非内容审计 | V1.0 |
| C | `POST /admin/debug-access-grants` / `{id}/commands/revoke` | 短时、理由、范围、明显banner | V1.0 |

管理员production A05不提供raw Prompt自由textarea；编辑/版本形成可在受控非生产authoring流程完成，生产仅registry/evaluation/promotion/revoke/rollback。
`/admin/config-bundles` 的 `type` 只接受 `SCENE_TEMPLATE/AGENT_TEMPLATE/REVIEW_RULE/COMPLIANCE_POLICY/PLATFORM_RULE`；Prompt、decision family、provider/model 与 price 使用各自专用资源。PromptConfig approve/config-deprecate只写其专用lifecycle metadata+receipt/audit；pilot/shadow/canary/active/revoke/rollback只写`prompt_activation` revision。二者均不能通过通用config endpoint形成第二权威。

## 6. SSE 合同

### 6.1 连接与恢复

- `GET /api/v1/events?taskId={optional}&cursor={optional}`；也支持 `Last-Event-ID`。两者冲突时按API ADR规定并返回明确错误。
- cookie认证；响应 `text/event-stream`, `Cache-Control: no-store`, proxy buffering disabled；连接有批准的最大时长/heartbeat。
- delivery至少一次，客户端按`eventId`去重；事件只是失效提示，不是业务事实或event sourcing。
- cursor过旧/权限变化返回明确 `CURSOR_EXPIRED/RESYNC_REQUIRED`，客户端重取work-home/task/active executions后以新cursor重连。
- API实例切换无需sticky；PG durable activity cursor保证恢复。Redis未来只可wake-up，丢通知后有界PG纠偏。

### 6.2 Event envelope

```text
id: 0000000000123456
event: resource.changed
data: {"schemaVersion":"flowverse.sse-event/v1","eventId":"uuid","cursor":"opaque","eventType":"RESOURCE_CHANGED","resourceRef":{"type":"EXECUTION","id":"uuid"},"resourceRevision":7,"taskId":"uuid","occurredAt":"2026-08-14T00:00:00Z","changeHints":["status","cost"],"errorCode":null}
```

允许类别：`RESOURCE_CHANGED`, `JOB_PROGRESS`, `CAPABILITY_CHANGED`, `EXPORT_READY`, `SESSION_EXPIRING`, `RESYNC_REQUIRED`, `HEARTBEAT`。不传正文、Prompt、evidence文本、评论、raw provider output、hash清单、secret或预签名URL。前端按resourceRef精确invalidate并GET权威状态。

## 7. API↔Worker 私有合同

### 7.1 边界与身份

- `/internal/v1`仅私网service endpoint，public Edge无route。
- Worker使用独立workload identity；不复用user/admin cookie；授权限定workload class和实例身份。
- 每个request带trace/request ID、worker build/schema capabilities；body严格Pydantic Schema，未知枚举/字段策略按版本合同。
- API和Worker不能形成业务调用环：Worker发起claim/heartbeat/result；现有API→Worker诊断需由ADR显式退役/隔离。

### 7.2 Endpoint catalog

| ID | Method/path | 请求关键字段 | 响应/不变量 |
|---|---|---|---|
| `INT-001` | `POST /internal/v1/workers/registrations` | workerId, buildVersion, supportedWorkloads/schemas, faultDomain, supportedPoolKeys | 短时registration/heartbeat policy与允许pool；不授予业务权利 |
| `INT-002` | `POST /internal/v1/workers/{id}/heartbeat` | capacity per class/pool, inFlight, deliveryStore free/oldest/health, stopClaim/retiring state | 当前capability与摘流诊断；不得用它改业务job结果 |
| `INT-003` | `POST /internal/v1/jobs/claims` | workerId, workloadClasses, poolKeys, maxJobs, supportedSchemas, supportedLeasePurposes, priorEmptyClaimCount | API按pool锁job、D重验并执行有界aging/fairness，返回0..bounded lease、`nextClaimNotBefore`，以及每job由服务端签发的`leasePurpose, jobContextRef/hash, leaseId, fencingToken, jobRevision, leaseExpiresAt`和封闭`jobContext`：AI=`executionPurpose + evaluationCallRole? + evaluationArm? + executionId/laneNo/attemptId/bindingId`（BUSINESS的role/arm均空；EVALUATION TARGET的arm=`CANDIDATE|CONTROL`；JUDGE arm为空），document=`objectVersionId`，export=`exportRequestId`，maintenance=`maintenanceType + deletionRequestId|recoveryCheckpointId`。正常为WORK；只有DeliveryStore有可枚举/校验的同context RESULT_BUFFERED record、无receipt且原WORK lease失效时才可签发DELIVERY_RECOVERY，并额外冻结original producer proof、reportEnvelopeRef/hash、deliveryRecordRef/hash与resultHash；只有删除屏障前已CALL_START_COMMITTED、普通WORK已fence且尚无buffer/receipt的同一intent，才可签发DELETION_DISPOSITION并冻结原producer proof、callIntent、deletionRequest/ledgerCursor/tombstoneRevision。context在job终态前稳定，lease/revision按响应推进 |
| `INT-004` | `POST /internal/v1/jobs/{id}/heartbeat` | heartbeatRequestId, heartbeatSequence, requestDigest, leasePurpose, jobContextRef, leaseId, fencingToken, expectedJobRevision, progress summary；AI context还带executionPurpose/evaluationCallRole?/evaluationArm?/laneNo/attemptId | 先按job_type与leasePurpose校验固定context，再延长有界lease并返回新的`jobRevision/leaseExpiresAt`，或明确`LEASE_LOST/CANCEL_REQUESTED/JOB_CONTEXT_MISMATCH`。API提交后响应丢失时，同`heartbeatRequestId+sequence+digest`必须返回首次已耐久的同一revision/expiry；同ID异digest冲突，旧sequence不得推进。DELIVERY_RECOVERY/DELETION_DISPOSITION均不能转成WORK；disposition只能在删除处置的有界期限内续租 |
| `INT-005` | `POST /internal/v1/jobs/{id}/call-starts` | `leasePurpose`, `jobContextRef/hash`, AI context的executionPurpose/evaluationCallRole?/evaluationArm?, laneNo, attemptId, stepId, bindingId, leaseId, fencingToken, expectedJobRevision, callIntentId, `resolvedCallInputManifestRef/hash`, requestHash, model/profile ref与provider idempotency capability/version | 仅`AI_EXECUTION+WORK lease`可调用，其他lease无条件拒绝；API在单一PG事务锁job/step并先校验purpose/arm/role/lane。BUSINESS重验匹配modelProfile activation+当时最新eligible assessment；EVALUATION重算并锁定typed authorization manifest/hash、expiry/revoke链、comparison mode/basis、EvaluationBinding/dataset/license/独立预算与`EVALUATION_ARTIFACT_ONLY`。TARGET调用输入必须由binding确定性产生；DIRECT JUDGE在candidate receipt前不可claim/call-start；PROMPT_ONLY PAIRED在两个provider TARGET arm及换位receipt齐全前不可进入；BASELINE_GATE在candidate receipt与typed baseline artifact/authority receipt齐全前不可进入且不创建control ModelCall；FACTORIAL按冻结factor/control plan检查。actual manifest逐项引用同一authorization/run内的所需artifact或baseline ref/hash/receipt并匹配selector、Schema与顺序；SHADOW还重验用户consent与rollout authority。两者都把resolved input与exact-key strategy写入`model_call`意图/receipt，提交后才返回短时授权及同一exact provider key。同intent/hash重领返回同一key；不支持幂等时不得自动恢复外部调用 |
| `INT-006` | `POST /internal/v1/jobs/{id}/progress` | `leasePurpose`, jobContextRef, leaseId, fencingToken, expectedJobRevision, reportKey, requestDigest, bounded stage/percentage/counts/safe message codes；AI另带stepId | 只接受WORK lease；AI校验execution/attempt/binding/step，document校验objectVersion，export校验exportRequest，maintenance校验封闭subtype与target；只追加无内容的可显示进度，不得携带payload、partial artifact、usage/cost、provider outcome、object locator或正文；写`PROGRESS/PROGRESS_ACCEPTED`最小report receipt，同key同digest重放同响应、异digest冲突。任何需保存的partial artifact必须走带DeliveryStore envelope/record的INT-007 `outputDisposition=PARTIAL`或含artifact INT-008 |
| `INT-007` | `POST /internal/v1/jobs/{id}/results` | leasePurpose, jobContextRef, leaseId, fencingToken, expectedJobRevision, `reportEnvelopeRef/hash`, `deliveryRecordRef/hash` | `requestDigest=reportEnvelopeHash`，当前WORK/DELIVERY_RECOVERY/DELETION_DISPOSITION acceptance tuple不在envelope内。API只从校验后的immutable envelope与delivery record读取purpose/role/arm/lane/step、`outputDisposition=PARTIAL|FINAL`、result/output manifest、usage/cost，transport不得另传第二份业务字段；若实现因协议便利重复携带，必须与canonical envelope逐字段/逐hash完全相等，任一差异返回409且不写owner/receipt。只接受已`RESULT_BUFFERED`的同context耐久交付记录；WORK按当前lease校验；DELIVERY_RECOVERY必须完全匹配claim冻结的原producer proof+report/delivery/result且无既有receipt，只允许交付该记录。DELETION_DISPOSITION还须匹配claim冻结的pre-barrier callIntent与deletion proof，只能写最小成本/审计、`DISCARDED_BY_DELETION` receipt和删除进度；两种特殊lease均禁止provider、新result或改变envelope。PARTIAL只保存不可变partial output/cost并保持job非终态，不创建semantic candidate/formal；FINAL BUSINESS AI可按严格Schema生成execution output/semantic candidate/cost。EVALUATION TARGET/JUDGE只写各自评测artifact/cost和run progress，严禁直接追加EligibilityAssessment或写business candidate/formal；只有API-owned evaluation-run finalizer在全部授权plan项、validator、hard-fail与必要人审闭合且无stale后，才以单一事务追加一个RUN_RESULT assessment revision。其他类型生成object verification/extraction、export artifact或维护进度。写`RESULT` report receipt并分别冻结producer/acceptance proof；普通WORK/RECOVERY若匹配task已有耐久ledger intent+PG tombstone，同样只走discard分支 |
| `INT-008` | `POST /internal/v1/jobs/{id}/failures` | leasePurpose, jobContextRef, leaseId, fencingToken, expectedJobRevision, reportKey, requestDigest；纯无artifact时携带同版canonical failure payload；含partial/usage/cost/provider outcome artifact时携带`reportEnvelopeRef/hash,deliveryRecordRef/hash` | 失败taxonomy、result/output manifest、usage/cost与purpose/role/arm/lane/step只从canonical payload/envelope读取；任何重复transport字段必须exact-match，否则409且不写owner/receipt。纯无artifact失败只接受WORK lease，其requestDigest按canonical payload计算，不建delivery record但写`FAILURE/FAILURE_ACCEPTED`最小report receipt。artifact失败可由WORK、完全匹配既有buffer的DELIVERY_RECOVERY，或匹配pre-barrier intent/deletion proof且只作discard的DELETION_DISPOSITION提交；后两者以reportEnvelopeHash为digest并禁止新provider/result/envelope。任何已`RESULT_BUFFERED` artifact按四类context校验；普通分支写`FAILURE+ACCEPTED`，删除交叉与disposition只保留批准的最小非内容成本/审计并写`DISCARDED_BY_DELETION`。均由API决定终态/人工恢复，Worker不能自动重试付费未知结果 |
| `INT-009` | `POST /internal/v1/jobs/{id}/delivery-acknowledgements` | workload identity, jobContextRef/hash, reportKey, deliveryRecordRef/hash, resultHash, result-or-discard receipt ref? | receipt-bound终态窄例外：只接受带delivery的RESULT或artifact FAILURE receipt，可在原lease过期、INT-007或含artifact的INT-008响应丢失、Worker重启后幂等重放；API先按UQ`(job_id,report_key)`取已耐久receipt，客户端ref若存在只作一致性校验，再严格验证同一job/context/delivery/result与`ACCEPTED|DISCARDED_BY_DELETION`状态，并按receipt kind校验WORK/DELIVERY_RECOVERY/DELETION_DISPOSITION的accepted lease proof，或DELETION_RECONCILIATION的maintenance/transaction proof、deletion request、ledger cursor与tombstone revision；PROGRESS/纯FAILURE receipt不得调用；只能推进`ACKNOWLEDGED/secure erase/GC`，不得写或修改owner result |
| `INT-010` | `GET /internal/v1/jobs/{id}/inputs`、`POST /internal/v1/jobs/{id}/input-grants` | GET携带workload identity、leasePurpose、jobContextRef、leaseId/fencing/expectedJobRevision且只返回immutable payload manifest和grant descriptors，不分配record或写状态。POST携带`grantRequestId,requestDigest`及同一lease tuple、requestedGrantPurpose、purpose/method/objectVersion/expiry/maxBytes；DeliveryStore写grant另带`reportType/reportKey/reportEnvelopeHash/resultHash` | GET按job_type返回最小输入引用：BUSINESS AI含activation/eligible-assessment/binding/input refs，EVALUATION TARGET含被测配置/dataset；DIRECT JUDGE只在candidate receipt齐全后返回candidate artifact+rubric/schema；PROMPT_ONLY JUDGE只在两个provider TARGET arm及换位receipts齐全后返回blinded CANDIDATE/CONTROL artifact+order manifest；BASELINE_GATE JUDGE返回candidate artifact与typed baseline artifact/authority receipt且绝不伪造control ModelCall；FACTORIAL按冻结factor/control plan返回声明的证据组合。所有resolved-call-input manifest都由API生成并可重算，逐项绑定同一authorization/run的artifact或baseline ref/hash/receipt且匹配冻结selector/judge schema。document/export/maintenance含各自封闭target/control manifest。所有短时read/write capability只由POST签发；grant command以`job+context+grantPurpose+grantRequestId`幂等，同ID同digest返回首次结果，同ID异digest 409。DeliveryStore record以`job+context+reportKey`唯一：首次原子冻结`reportEnvelopeHash/resultHash/deliveryRecordRef`，此后即使使用新grantRequestId，同key同两hash也只返回原record/可续grant，任一hash或digest不同均409且不得签第二record/grant或写payload。正常WORK预分配稳定`deliveryRecordRef`并返回`DELIVERY_BUFFER_CREATE`单record/no-overwrite grant。删除barrier后普通WORK无写grant；仅pre-barrier `CALL_START_COMMITTED`且持有效DELETION_DISPOSITION lease的同一intent可取得绑定deletionRequest/ledgerCursor/tombstoneRevision与隔离前缀的`DELETION_DISPOSITION_BUFFER`。DELIVERY_RECOVERY只能取得claim冻结的exact reportEnvelope/deliveryRecord读取grant；两种特殊lease均禁止原输入、普通写grant或provider secret。所有grant禁止list/任意key；过期续签使用新grantRequestId并仍重验同一record与当前门，不自动放宽 |

`job-report-envelope/v1`的canonical payload固定为`schemaVersion,reportType,reportKey,jobId,jobContextRef/hash,producerLeaseId/fencingToken/jobRevision,executionPurpose/evaluationCallRole/evaluationArm/lane/step(适用),outputDisposition(PARTIAL|FINAL，RESULT适用),resultHash(artifact适用),typedOutputManifest|failureTaxonomy,usage/cost refs`。它**不得包含**`deliveryRecordRef/hash`，从而避免信封与delivery record的哈希自引用；`requestDigest=hash(canonical envelope)`。当前WORK、DELIVERY_RECOVERY或DELETION_DISPOSITION acceptance lease/fencing/revision、传输时间和重试次数明确排除在digest外，另存进receipt的acceptance proof；原producer proof仍属于envelope且不可改写。PROGRESS和纯无artifact FAILURE可内联同版canonical payload；RESULT与含artifact FAILURE必须把该envelope作为DeliveryStore不可变记录的一部分，由服务端预分配的delivery record单向保存`reportEnvelopeRef/hash`并生成自己的`deliveryRecordHash`，恢复者只能复用原两组ref/hash。DeliveryStore record固定`initialState=RESULT_BUFFERED`但不把后续可变状态写回hash；`REPORTED/ACKNOWLEDGED/SECURE_ERASED/GC`是append-only transition序列与可重建current projection，receipt和INT-009始终校验原envelope hash、record hash及单调状态链。

### 7.3 Lease/fencing状态

AI typed context在claim、heartbeat、call-start、progress、result、failure、DeliveryStore envelope/record和receipt中必须逐字段保持`executionPurpose + evaluationCallRole? + evaluationArm? + laneNo + attemptId + bindingId + stepId?`一致：BUSINESS的role/arm均为空；EVALUATION TARGET的arm为`CANDIDATE|CONTROL`；JUDGE的arm为空。任何投影不得省略arm后再靠binding反推或默认。

`AVAILABLE → LEASED → RUNNING → RESULT_BUFFERED/terminal`，可有`CANCEL_REQUESTED/WAITING_USER/PARTIAL/OUTCOME_UNKNOWN/WAITING_DIAGNOSIS/RETIRED`。`INT-004..INT-008`先校验共同的`jobId + jobContextRef + leasePurpose + leaseId + fencingToken + expectedJobRevision`；随后按`job_type`判别：AI固定`execution→lane attempt→binding+executionPurpose`且call/progress/result适用时固定step，document固定objectVersion，export固定exportRequest，maintenance固定封闭subtype与deletion request或recovery checkpoint。只有AI+WORK lease可进入JIT call-start；BUSINESS与EVALUATION共用外部副作用安全链，但前者的activation/eligibility门和后者的evaluation-authorization门不可互换。普通lease expiry只允许无外部副作用且合同证明安全的WORK重新领取；已越过JIT边界的AI step除非provider明确支持并验证同一exact idempotency key，否则不自动重放。若artifact已RESULT_BUFFERED但首次report前producer崩溃/lease失效，只能签发DELIVERY_RECOVERY交付原record；若删除barrier前已CALL_START_COMMITTED而尚未buffer，只能签发DELETION_DISPOSITION把已有outcome写入隔离record并取得discard receipt。两者都不能调用provider、修改原result或产生业务事实。所有intent/report key幂等；任一context/purpose/step/lease/revision不匹配返回`409/LEASE_LOST|JOB_REVISION_CONFLICT|JOB_CONTEXT_MISMATCH|ATTEMPT_STEP_MISMATCH`，不得调用provider或写任何owner result/cost/candidate。`INT-009`是唯一不要求当前active lease tuple的terminal-after-receipt例外；它按`job+reportKey`找回已经提交但响应可能丢失的receipt，只能以其中冻结的producer/acceptance proof做ACK/secure erase/GC，不能复开job或新增业务事实。

### 7.4 Claim、退避、公平、摘流与 DeliveryStore

- AI delivery record与unreceipted index使用与7.3相同的完整typed context，canonical hash必须包含purpose/role/arm/lane/step/binding/callIntent；恢复、删除处置和ACK均只允许重放原arm，禁止把CONTROL结果当CANDIDATE或反向替换。
- API是唯一claim调度owner；Worker在`nextClaimNotBefore`前不得紧轮询。连续空领取、429/503和连接失败分别使用有界指数退避+jitter，精确起始/上限/总时长保持Proposed，且同一调用链只能有一层自动重试。
- claim先受`pool_key`容量隔离，再在允许pool内按到期时间、优先级和有界aging/fairness选择；`SKIP LOCKED`只解决并发占有，不等同公平调度。必须用“持续注入高优先级+低优先级哨兵job”证明无饥饿后才可声称通过。
- 每个含artifact的Worker result/failure在首次report前都必须write-through到批准的耐久交付介质并取得`RESULT_BUFFERED`记录，不以“API当前看起来可用”跳过。delivery record的canonical hash**单向**冻结`reportEnvelopeRef/hash`、服务端预分配的deliveryRecordRef、job+typed context、result hash、producer proof、created/expiry和`initialState=RESULT_BUFFERED`；report envelope绝不反向包含record hash。AI另冻结purpose/role/lane/step/binding/callIntent，document绑定objectVersion，export绑定exportRequest，maintenance绑定封闭subtype+deletionRequest或recoveryCheckpoint；删除处置buffer还冻结deletionRequest/ledgerCursor/tombstoneRevision并处于业务不可读隔离前缀。恢复Worker只能重放这些已冻结值，不能重生成key/digest。payload可位于加密DeliveryStore或满足同等耐久/完整性合同的immutable ObjectStore version，但必须有同一delivery record。DeliveryStore还须给API reconciliation提供鉴权、有界、稳定snapshot/cursor的unreceipted index；index以`job/context/reportKey`唯一，具有单调sequence/HWM，且payload+immutable report envelope+delivery record+index entry必须在同一DeliveryStore durability boundary成功后才返回RESULT_BUFFERED。reconciliation和删除cleanup只有在所有pre-barrier intent/写grant收口后捕获固定scan HWM，完整分页处理、无gap/迟到entry且所有匹配record有receipt+ack/erase后才能完成；index不可验证、lag越门或分页中断时对应pool与cleanup fail closed，不能依赖Worker进程或无界bucket list发现。
- Worker摘流顺序为`stop-claim → heartbeat RETIRING → 有界完成安全工作 → 确认所有artifact RESULT_BUFFERED → report → API result-or-discard receipt → delivery ack/清理 → lease释放或到期 → TERMINATED`。producer在buffer后、首次report前丢失时，API reconciliation以unreceipted index建立DELIVERY_RECOVERY候选并由新lease仅交付原record；不得以进程退出或API低延迟代替结果交付/fencing。
- DeliveryStore不是业务权威或第二队列。含artifact的result/failure只有在API返回耐久receipt且INT-009 ACK后才能删除；正常结果要求`ACCEPTED`，删除交叉要求`DISCARDED_BY_DELETION`并安全擦除。纯无artifact failure仍写`FAILURE_ACCEPTED`；删除时无本地payload的已提交call必须写可验证`NO_PAYLOAD_DISPOSITION_ACCEPTED`，不能把“索引里没找到”本身当作证明。满载、损坏、超期、重复投递和API长时不可达进入诊断/告警并停止对应pool；不能靠TTL或空间压力越过处置门。
- `INT-010` 是所有 Worker 业务输入与对象 grant 的唯一获取/续签入口；claim 不携带 locator/secret。普通grant过期时只能在同一active lease/revision/purpose下续签；取消、删除、policy revoke、context漂移或对象状态不再允许时拒绝续签并由 Worker 有界收口，绝不改用管理员凭据、bucket listing或缓存旧URL。删除屏障后的唯一写例外是上述`DELETION_DISPOSITION_BUFFER`，只能服务barrier前已开始intent，不能恢复普通输入能力或创建业务可读结果。

## 8. 对象上传/finalize/处理协议

### 8.1 Create session response

返回logical `objectId/objectVersionId/uploadSessionId`、允许method、短expiry、maxBytes、required headers摘要和opaque upload capability。不得返回管理员credential或允许list bucket/任意key。

### 8.2 Finalize command

body包含session/object/version、客户端观察到的size/hash（仅声明）、expected session revision；相同command幂等。API封存session，拒绝过期/覆盖/version漂移，并创建verification job。此时对象仍quarantine、不可下载/解析/入模。

### 8.3 Verification/result

Worker流式读取指定immutable version，计算actual SHA-256/size/MIME，验证扩展名、压缩展开/页数/字符数/嵌套、hash/version/session binding。API接受结果后写权威metadata，才进入`VERIFIED/PROCESSING/COMMITTED`。解析失败可形成`PARTIAL/REJECTED`业务状态，但不能通过重复finalize绕开。

### 8.4 当前事实与 ObjectStore DataSafety/Availability 放行门

- 当前只确认单主机 MinIO 服务曾达到基础健康；最新本地认证诊断仍为 `InvalidAccessKeyId`，因此业务upload/finalize/download/Worker-read均为 **Unverified/disabled**。健康端点、管理凭据或能列bucket都不能替代应用identity的live contract证据。
- 强制的首个H0对象/DataSafety切片前必须用非管理、最小权限的业务identity，且批准TLS/加密、凭据轮换、bucket/purpose隔离、容量/配额/生命周期、备份/版本；contract suite覆盖quarantine写、指定immutable version读、服务端hash/size/MIME核验、commit后授权读、越权/列bucket/覆盖拒绝、短时grant过期、删除/ledger、Range/deadline/cancel、adapter错误归一化，以及ADR-0018一致恢复/不复活/restore演练。失败时只关闭对象相关capability，PG正文与安全查询保持可用。
- 跨批准故障域耐久、副本故障包络和N-1证据只在`UD-AVL-01`使`AvailabilityGate`适用于该发布或可用性声明时到期。未适用不能阻断基础H0，但也不得把当前MinIO地址、bucket/key、单节点volume直接写入公开合同或宣称生产HA/N-1/99.9%；无论是否适用都不能豁免上一条DataSafety。

## 9. AI binding 与 SemanticFinding 合同

Canonical模型payload、family registry、三binding与activation状态只由 [SYSTEM_DECISION_PROMPTS.md](../ai/SYSTEM_DECISION_PROMPTS.md) 定义。数据/API实现必须保持：

0. 所有AI执行与评测权威引用都显式携带`executionPurpose/evaluationCallRole?/evaluationArm?`；BUSINESS二者均空，EVALUATION TARGET要求arm，JUDGE arm为空。该判别在Preview、Binding、JobContext、ModelCall、report envelope、DeliveryStore、receipt与finalizer之间逐项一致，不允许由客户端省略后让服务端猜测。

1. `PromptConfigBundle`、`EvaluationBinding`、`ExecutionBinding`三者独立不可变；activation key=`environment + familyId + activationScope + modelProfileId`，同一family可为获准的不同精确模型各保有一个champion/LKG，但同一完整key只能一个Active。EvaluationBinding冻结DIRECT或带明确basis/control/change-set/blind-order的PAIRED定义，当前证据/资格来自其`evaluation_run` append-only assessment stream的最新有效revision，不能回写binding。Prompt变更晋升默认要求与verified LKG匹配的PROMPT_ONLY PAIRED或获批FACTORIAL；首版用BASELINE_GATE，V1的DIRECT只能补充而不能独立晋升。为消除“未评测不得激活、未激活无法评测”的循环，ExecutionBinding以`BUSINESS/EVALUATION`判别：BUSINESS每lane必须绑定匹配该modelProfile的active revision与最新eligible assessment；EVALUATION必须绑定typed immutable authorization receipt和同一EvaluationBinding，禁止要求或伪造activation/eligible assessment。`OFFLINE_EVALUATION`由管理员评测命令授权；`SHADOW_EVALUATION_CONSENT`同时要求rollout authority与用户D01 consent。TARGET/JUDGE各匹配冻结配置与Schema，输出永不成为业务candidate/formal。
2. ExecutionBinding在provider call前有canonical hash并冻结purpose/basis/role/arm对应权威依据；JUDGE binding冻结basis-specific依赖选择器而不伪造未来artifact hash。每个provider调用还必须经过原子JIT call-start提交边界。Worker以当前lease/fencing提交`executionPurpose+comparisonBasis?+evaluationCallRole?+evaluationArm?+lane+callIntentId+resolvedCallInputManifestRef/hash+requestHash`；API在同一PG事务锁定job/attempt/step/binding归属。BUSINESS锁定最新assessment revision并重验绑定activation的真实性及是否被安全撤销/失格；EVALUATION锁定typed immutable authorization receipt并重验kind/actor/manifest/hash/expiry/revoke、EvaluationBinding/dataset/license/独立预算及无业务写capability，OFFLINE验证管理员authority，SHADOW验证rollout authority与用户D01 consent，provider TARGET只匹配真实PromptConfig；JUDGE只有在basis所需artifact或typed baseline authority receipts齐全后才能claim/call-start，实际输入manifest须逐项匹配同一run的artifact/baseline ref/hash/receipt与binding selector。两者都重验policy/price/budget、input/object引用、取消/删除状态，把JIT实际输入和assessment或evaluation-authorization ref/hash/kind/basis/role/arm写入不可变`model_call`意图和幂等receipt后才返回短时单用途授权。事务失败、purpose/basis/role/arm/lane/input/ref/hash漂移或严重安全撤销均不得调用provider；仅出现更新的正常activation revision不会改写或自动否定已经运行的BUSINESS attempt。
3. 只有BUSINESS decision-family模型返回`SemanticFindingCandidate`公共body：status/findings/contradictions/missingEvidence/humanReviewReasonCodes/familyPayload；familyPayload由familyOutputSchemaVersion且`additionalProperties=false`校验。EVALUATION TARGET/JUDGE使用各自冻结的evaluation-artifact schema，不创建SemanticFindingCandidate或business formal。
4. 对BUSINESS语义候选，执行器追加唯一canonical `semantic-candidate-envelope/v1`：`schemaVersion,familyId,promptVersionId,promptConfigRef,promptConfigHash,evaluationBindingRef,evaluationBindingHash,executionBindingRef,executionBindingHash,inputManifestHash,activationRevision,validationStatus,rawOutputHash,validatorVersion,validatorResult,createdAt,modelPayload`，并按第2节持久化于ExecutionOutput；EVALUATION不冒用该envelope。面向UI的脱敏投影必须使用不同名称/版本（候选`semantic-candidate-view/v1`），不得复用可信envelope名称。
5. 任何引用不存在、manifest外证据、hash/revision不符、未知枚举/字段、非法action或Schema失败使整份candidate无效；不得择取“看起来合理”的字段。
6. 模型无最终PASS/BLOCK、capability、权限、Cycle有效性、comparability、预算、激活、formal或mutation权限。
7. call-start提交后即按“外部调用可能发生”处理：授权响应丢失、Worker崩溃或lease过期不得盲重放；只有provider明确支持且服务端能重建/解密并验证同一exact idempotency key时才可沿同一call intent恢复，否则进入`OUTCOME_UNKNOWN/WAITING_DIAGNOSIS`。撤销只阻止尚未越过该边界的新调用，绝不静默把既有ExecutionBinding换成LKG；需要换配置/模型时创建新preview/binding/attempt。

## 10. 兼容、生成物与验证门

### 10.1 合同生成链

批准后推荐：领域值对象/状态与Pydantic transport schema → reviewed OpenAPI `/api/v1`/internal文档 → deterministic TypeScript DTO generation → frontend adapter/ViewModel。数据库模型不直接生成公开DTO，OpenAPI也不能反推domain/DDL。

生成物必须可重复、提交或在CI可验证，拥有版本、diff和breaking-change gate。unknown fields可忽略；unknown enum必须进入安全unknown/read-only，不默认PASS/ACTIVE/VALID。

### 10.2 Proposed 逐版物理 allowlist

为避免把累计路线图一次性物理化，本节给当前目录定义可机械核对的序号：`T001..T103`是第2节从上到下的 **103行逻辑表**；`PUB-001..PUB-107`是第5节从上到下的 **107行业务Public endpoint catalog**；`INT-001..INT-010`是第7.2节的 **10行business internal endpoint catalog**；`OPS-API-001..003/OPS-WORKER-001..002`是第4.5节的 **5行独立operational allowlist**，不计入PUB。业务目录一行可包含同资源的query/command组合；生成OpenAPI/internal contract时必须展开该行列明的每个method/path。序号、规范化行文本和本文revision/hash必须一起写入未来release manifest；目录增删/重排会使旧manifest校验失败并要求重新审批，不能靠范围悄悄吸收新能力。

| Gate | 新增表候选（精确集合） | 新增业务Public目录行候选（精确集合） | Internal/operational路由与版本overlay | 数量核对 | 状态 |
|---|---|---|---|---|---|
| H0 / V1.0 | `T001–T007, T009–T060, T087–T103` | `PUB-001–PUB-021, PUB-025–PUB-066, PUB-092–PUB-107` | `INT-001–INT-010`且只允许H0 job/family/schema/capability；`OPS-API-001..003/OPS-WORKER-001..002`独立保留 | 76 tables；79 business Public rows；10 Internal rows；5 operational rows | Proposed / Unverified |
| H1 / V1.1 delta | `T008, T061–T080, T084` | `PUB-022–PUB-024, PUB-067–PUB-085, PUB-089` | 无新增path；只扩H1 family/schema/capability | 22 tables；23 Public rows；0 new Internal rows | Proposed / Unverified |
| H2 / V1.2 delta | `T081–T083, T085–T086` | `PUB-086–PUB-088, PUB-090–PUB-091` | 无新增path；只扩H2 family/schema/capability | 5 tables；5 Public rows；0 new Internal rows | Proposed / Unverified |
| V1 cumulative check | H0+H1+H2=`T001–T103` | H0+H1+H2=`PUB-001–PUB-107` | `INT-001–INT-010` overlay逐版累计；5行operational集合不随业务版本扩张 | 103 tables；107 business Public rows；10 Internal rows；5 operational rows，no gap/overlap | Proposed / Unverified |

这些集合是“首次到期候选”，不是DDL/OpenAPI批准或实现声明。每个gate的物理manifest仍须展开表的列/约束/索引/owner、endpoint的完整method/path/schema/auth/idempotency/status、event/UI route/Prompt family/migration/test，并经owner与ADR接受；未列入当前gate的实体、字段、枚举分支和路由必须在migration、runtime capability和deep link三层fail closed。共享表/路由还需以下版本overlay：H0的`stage0_draft`只允许`CREATION`且不启用operation字段；H1才启用`OPERATION`、release/feedback/analysis/decision；H2才启用iteration/comparison/value及Cycle N+2路径。Internal路由虽在H0一次建成，H0只接受`AI_EXECUTION/DOCUMENT_PROCESSING/EXPORT_GENERATION/MAINTENANCE`四个job type；`MAINTENANCE`仅允许`DELETION_RECONCILIATION/RECOVERY_CHECKPOINT_BUILD`两个subtype与对应typed target，不是任意脚本入口。H1/H2不新增job type，只累计各自获批Schema与capability。未知job type/subtype、family、schema version或未到期capability均在registration、claim和report三处拒绝。

系统决策family的逐版overlay同样是精确集合：H0=`PF10-INTENT-ROUTE, PF10-CREATION-BASELINE-EXTRACT, PF10-REFERENCE-RISK, PF10-CONTENT-REVIEW, PF10-DISAGREEMENT, PF10-MEMORY-DELTA, PFX-COMPLIANCE-SEMANTIC`；H1 delta=`PF11-OPERATION-BASELINE-EXTRACT, PF11-PACKAGE-REVIEW, PF11-RELEASE-DIFF, PF11-EXTERNAL-EVENT, PF11-FEEDBACK-TEXT-RISK, PF11-EVIDENCE-ANALYSIS, PF11-NEXT-ACTION-OPTIONS, PF11-HUMAN-DECISION-DRAFT`；H2 delta=`PF12-DECISION-TO-PLAN, PF12-CHANGE-IMPACT, PF12-CYCLE-COMPARISON`。正文/包装内容生成不是这些decision family，其独立Schema未获批准前不能因`AI_EXECUTION`路由存在而启用。现有Bootstrap Web Check page、`GET /api/v1/system/chain`和`GET /internal/v1/system/status`均不属于业务`PUB/INT`目录；production H0必须成对移除/不注册或返回`404/410`并以依赖图/测试证明API不再调用Worker。三者只可在明确隔离、非生产的diagnostic profile按ADR-0005成对保留，不能参与business/operational readiness或capability；第4.5节5个`OPS-*`健康路由独立保留且不得调用该诊断链。

未来release manifest必须同时给出deny list和四项自动断言：物理Schema不得出现不属于累计集合的表/列/enum；业务public router/OpenAPI不得出现不属于累计PUB集合的method/path；internal router及registration/claim/report不得接受未到期的path/jobType/subtype/family/schema/capability；operational router只能出现第4.5节5条且production profile不得出现诊断三件套或API→Worker调用。H0 benchmark只在H0实际物理集合及其批准fixture上运行，不能用103/107/10/5累计目录制造通过或容量结论。

### 10.3 数据/API测试

- migration head、empty→head、代表性upgrade、forward-fix/restore、不可逆点检查。
- 每张表的PK/FK/UQ/CK/partial unique、append-only和跨task/actor越权测试。
- concurrent revision/idempotency/slot/claim/ActualRelease+Cycle和ledger-first crash-point测试。
- API envelope/error/status/cursor/unknown enum、CSRF/session/role/admin/internal隔离，以及同一`/health/ready`的PUBLIC/INTERNAL受控audience scope、独立pool故障不交叉摘流和客户端伪造scope拒绝。
- SSE duplicate/gap/cursor expiry/reconnect/slow client/capability change。
- Worker测试覆盖四类typed context、heartbeat/grant/report幂等与响应丢失、同reportKey异hash拒绝、grant越权、普通/处置buffer、stale fencing、BUSINESS/EVALUATION arm+role、DIRECT/PAIRED TARGET→JUDGE依赖与resolved input、多lane、JIT、failure/unknown、retire、DeliveryStore/HWM/recovery及删除收口；特别覆盖有payload的pre-barrier call晚到→DELETION_DISPOSITION，以及无payload→全部lease/grant失效+固定HWM无record后唯一`NO_PAYLOAD_DISPOSITION` proof。late payload与no-payload finalizer并发只能一个终态，cleanup不得提前COMPLETE。
- object quarantine/finalize/overwrite/range/hash/MIME/zip bomb/orphan/delete/restore。
- three binding/envelope/schema/reference/activation/revoke/LKG/no-AI contract。

### 10.4 实施前批准项

- API/Schema/auth/object/async/provider ADR accepted；`execution_control`等新增边界进入Architecture Baseline。
- 所有表名/列/类型/enum/retention、跨owner FK、immutability enforcement和physical index经data owner批准。
- OpenAPI endpoint/header/status/error/cursor/idempotency scope/digest/receipt retention经API/Web/Worker owner共同批准。
- 新依赖精确版本/许可证/命令进入TECH_STACK且Confirmed+Available。
- privacy/security、性能负载、HA/recovery、UIUX/AC traceability有到期测试计划。

## 11. 明确不建的表与接口

- `workflow`, `dag`, `agent_plugin`, `prompt_marketplace`, `custom_tool`, `dynamic_ui_schema`。
- `tenant`, `organization`, `team_membership`, `subscription`, `payment`。
- `broker_event`, `event_store`, 全量domain event sourcing或独立CQRS数据库。
- `vector_embedding`, `timeseries_metric`, `hypertable`, 金融instrument/market/fundamental/portfolio/backtest。
- 自动平台登录/credential、自动publish/withdraw/scrape endpoint。
- 通用 `/execute`, `/admin/impersonate`, `/confirm-anything`, `/bypass-compliance`。

## 12. 本文验证边界

本文只创建评审稿，未运行DDL/migration/OpenAPI/client generation、数据库integration、API contract、业务E2E、性能、HA或restore测试；上述能力均为`Unverified`。回退本文只删除本文件，不影响代码、数据库或外部环境。
