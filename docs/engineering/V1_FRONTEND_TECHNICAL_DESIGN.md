# FlowVerse V1 前端技术详细设计（评审稿）

## 0. 状态与边界

**状态：`IN_REVIEW / PROPOSED`。**

本文定义 Web SPA 的技术实现候选，不修改 `services/web`，不批准依赖或声称 UIUX 已实现。当前 Confirmed 事实只有 [TECH_STACK.md](TECH_STACK.md) 登记的非业务 Bootstrap；产品 Router、query/form/IndexedDB、E2E、视觉和无障碍工具都要单独锁版。

前端不拥有权限、Cycle有效性、预算、合规、Prompt activation、正式状态或唯一下一步公式。它展示 [数据与接口合同](V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md) 的服务端权威资源/capability/receipt，并在 owning page 收集人类明确提交。

## 1. 技术栈

| 能力 | 当前/建议 | 状态 |
|---|---|---|
| Runtime | Node.js 24.17.0、pnpm 11.10.0 | Confirmed bootstrap |
| UI/build | React/React DOM 19.2.7、TypeScript 5.9.3、Vite 8.1.4 | Confirmed bootstrap |
| Test/quality | Vitest 4.1.9、ESLint 10.6.0、Prettier 3.9.5、typescript-eslint 8.63.0 | Confirmed bootstrap |
| Routing | React Router候选 | Proposed；精确版本、route API、bundle/安全审查待批 |
| Remote state | TanStack Query候选 | Proposed；取消、重试、stale、SSE失效策略待批 |
| Form/schema | React Hook Form + Zod候选 | Proposed；服务端Pydantic/OpenAPI仍权威 |
| Local draft | IndexedDB + `idb`类薄repository候选 | Proposed；不把localStorage/query cache当草稿耐久 |
| API DTO | OpenAPI TypeScript generator候选 | Proposed；DTO→ViewModel adapter隔离生成类型 |
| Editor | 章节级plain text/批准Markdown子集 | Proposed；首版无富文本/协同框架 |
| Realtime | 原生EventSource/SSE | Proposed；有界轮询降级，不用WebSocket |
| E2E/a11y/visual | Playwright + axe类候选 | Proposed；必须覆盖130场景和批准viewport |

不引入UI组件库、全局业务状态库、微前端、动画框架、Service Worker缓存、动态UI renderer、Workflow/DAG库或富文本插件平台。若后续证据要求引入，必须有新依赖与迁移评审。

## 2. 目录与依赖方向

```text
src/
  app/                 # composition root, router, providers, error boundary
  routes/              # route descriptors/load boundaries; no domain logic
  shell/               # auth/user/admin shells, layout, responsive capability
  features/
    auth/
    work-home/
    task/
    stage0/
    references/
    creation/
    review/
    execution/
    release-cycle/
    feedback-decision/
    governance/
  entities/            # stable UI-facing refs and pure ViewModel types
  shared/
    api/               # generated DTO + hand-written client/adapters/errors/SSE
    ui/                # local accessible primitives
    tokens/            # canonical→semantic design tokens
    forms/             # field/error infrastructure, not business schemas
    drafts/            # IndexedDB repository/migrations/conflict records
    telemetry/         # privacy-safe client signals
    utils/
```

依赖方向：`app/routes → feature composition → entity/shared ports`；feature之间不导入内部component/store/hook。跨feature跳转通过route descriptor和stable resource ref，不通过共享mutable store。`shared/api/generated`不能被页面直接渲染，先在feature adapter转成ViewModel。

禁止：`shared/business-utils`万能目录、任意feature读取另一feature query cache内部key、复制后端枚举为无来源字符串、在组件里拼MinIO/provider URL、从SSE payload直接修改正式状态。

## 3. Route、版本能力与页面合同

具体pathname仍为Proposed；UIUX ID是稳定产品surface标识。建议 route descriptor：

```ts
type RouteDescriptor = {
  routeId: string;
  surfaceId: "AUTH" | "P01" | "STAGE0" | "P02" | "P03" | "P04" | "P05" | "ADMIN";
  requiredRole: "ANONYMOUS" | "USER" | "ADMIN";
  introducedIn: "V1.0" | "V1.1" | "V1.2";
  resourceRefs: readonly string[];
  mobileMode: "FULL" | "READ_ONLY" | "SIMPLE_SURVEY_ONLY";
};
```

服务端 `/capabilities` 决定route/action当前是否introduced/enabled/blocked，并可向官方renderer返回当前route/layout的短时 `presentationCapabilityRef`；该ref只防止官方Web在resize/route变化后陈旧提交，不证明物理viewport或设备，也不是恶意客户端安全边界。前端build flag只能帮助发布，不能是唯一业务事实。未知deep link安全失败，不创建对象。

| Surface | Proposed route pattern | 主要查询 | 允许写入/命令 | First |
|---|---|---|---|---|
| AUTH | `/login`, `/password-change` | session | login/password/logout | V1.0 |
| P01 | `/work` | work-home, tasks, pending, activity | new task, Bot message候选；action card只导航 | V1.0 |
| Stage0 | `/tasks/:taskId/stage0/:part` | task/baseline/draft/capability | save draft、confirm/replace owning baseline | V1.0/V1.1 |
| P02 | `/tasks/:taskId` | cockpit, next action, cycles, budget | D10 desktop/compact only; delete intent | V1.0 |
| P03 | `/tasks/:taskId/create/:tab` | refs/content/candidates/review/memory/versions/executions | upload/save/select/review/formalize/memory/execute | V1.0；decision-driven V1.2 |
| P04 | `/tasks/:taskId/release/:tab` | packaging candidates + current/history/by-id formal PackagingVersion、plan/release/cycle/feedback | confirm packaging/plan/release/event/feedback | V1.1 |
| P05 | `/tasks/:taskId/review/:tab` | analysis candidates + current/history/by-id FormalAnalysis、decision/comparison/value | formal analysis/human decision/plan/survey | V1.1/V1.2 |
| ADMIN | `/admin/:module` | accounts/config/eval/jobs/audit | role-scoped admin commands；无user formal handlers | V1.0 cumulative |

P01 Bot 使用服务端 `bot_conversation/message/action_card/unapplied_draft` 资源；history/context revision/expiry 和付费 execution 独立于 work-home 其他 section。action card 只导航，未应用 draft 只能经 owning page 变成普通可编辑表单草稿。高级设置使用 `execution_preference_version`，显示其 CreationBaseline 边界；越界只能导航 Stage0 replacement。A05 对每个 lifecycle transition 使用独立命令与 receipt，不把 approve/pilot/shadow/canary/active/revoke/rollback 合成一个万能开关。

P05的next-round/comparison/value在V1.1是`Not introduced`，不是“填完某字段即可解锁”。V1.2 entry只需eligible HumanDecision/task/baseline，iteration plan在进入后产生。

## 4. 状态所有权

| 状态 | 唯一owner | 前端保存位置 | 规则 |
|---|---|---|---|
| URL/navigation | Router | URL/history | 可分享非敏感定位；不放token/正文/filter PII |
| server query | API | query cache（可丢） | resource/revision key；重取权威；不得离线formal |
| form/edit buffer | owning form/controller | component/reducer + IndexedDB适用草稿 | dirty/validating/saving/saved/conflict/offline分开 |
| Shell/Bot/drawer | app/shell | React context/reducer | 只管理展示，Bot失败不影响确定性入口 |
| formal capability | API D layer | response only | 前端不计算；每次command提交D2重验 |
| execution progress | API authority | SSE hint + query | SSE只invalidate；不重演状态机 |
| DecisionCandidate | API validated candidate | query data + local unsaved review | candidate/abstain/needs human review；不成为action |
| offline draft | browser draft repository | IndexedDB | account/task/object/revision/schema隔离；不视为加密保险箱 |
| secret/session | API/cookie | HttpOnly cookie不可读 | 不进local/session storage；CSRF token按批准方案 |

不为“方便”建立全局Task/Cycle store。多个页面需要相同数据时，共用API resource query与adapter，不共享可变domain object。

## 5. API Client

### 5.1 Transport pipeline

`generated DTO → runtime envelope/schema guard → normalized ApiResult/Error → feature adapter → ViewModel`。

- 所有fetch有AbortSignal和deadline owner；route切换/新save取消旧的安全请求。
- GET只有在服务端`retryable=true`、该endpoint的自动重试策略和次数/总时长预算均已批准时，才由一个client owner执行有界backoff+jitter；429/503存在`Retry-After`时必须服从。当前预算未冻结时默认零自动重试并提供手动安全恢复。没有权威响应的transient transport failure也默认手动；若未来需要自动重试，必须在OpenAPI endpoint metadata与客户端policy中另行批准，不能由query库自行分类。401/403/404/409/422、Schema/权限/业务拒绝不自动重试。
- 正式command不由query库自动重试。网络结果未知先GET receipt；只有相同Idempotency-Key+digest可安全重发。
- `X-Request-Id`用于支持关联；错误显示用户文案和errorId，不展示stack/provider body。
- response unknown field可忽略；unknown enum/Schema failure产生`UNKNOWN_SERVER_STATE`，相关正式CTA禁用并可重取/反馈。
- content、Prompt/raw output、download grant使用`Cache-Control:no-store`并避免持久query cache。
- query、receipt与error必须先通过共通恢复字段guard：`degradationMode, affectedCapabilities, dataFreshness, asOf, lastKnownGoodRef, retryable, retryAfter`。缺字段、未知enum或`CURRENT`与资源revision/asOf矛盾均视为`UNKNOWN_SERVER_STATE`，禁用formal/release/decision/AI/object-finalize；`VERIFIED_LAST_KNOWN_GOOD`必须有可授权ref及asOf，仍只读。不得由本地cache自行推断“已恢复”。

### 5.2 Query key

以稳定资源而非URL字符串散落：`["task", taskId]`, `["creativeObject", id, projection]`, `["execution", id]`。SSE `resourceRef/revision/changeHints`只invalidate精确key。mutation receipt返回的resultRefs先invalidate再GET，不直接把payload拼成权威cache。

### 5.3 Pagination

列表使用opaque cursor；前端不解码、不把offset当稳定位置。筛选/排序改变清空cursor；新事件不自动跳用户滚动位置，显示“有新内容”再刷新。正文按对象/版本独立请求。

## 6. SSE Client

单session最多一个共享EventSource owner；订阅结果在client event bus中只发送typed invalidation，不发送业务状态。

1. 连接携带cookie与最后cursor；记录连接状态但不显示“系统成功”。
2. event runtime validate；重复eventId丢弃；revision小于已见revision可忽略，大于1并不证明丢失但触发GET。
3. `RESYNC_REQUIRED/CURSOR_EXPIRED`重取work-home、当前task、active executions并以新cursor重连。
4. 浏览器原生重连之外需有批准的backoff/connection上限，避免多tab风暴；多tab协调若无证据不预建复杂leader。
5. SSE不可用降级为页面可见时的有界轮询/手动刷新；最长10s状态更新产品目标仍需测量。
6. logout、account switch、task deletion完成立即关闭stream和清query/local data。

## 7. 表单、编辑器、草稿与冲突

### 7.1 表单状态机

`pristine → dirty → validating → saving → saved`；旁路状态：`save_failed`、`offline`、`stale/conflict`、`blocked`。保存失败保留字段和焦点；formal CTA只有server latest save receipt/revision、页面validator和capability均满足才enable。

- 浏览器做格式/即时校验；服务端错误按stable field path/reason code映射。浏览器“valid”不是服务器可确认。
- Stage0 AI extractor的字段必须标`USER_PROVIDED/REWRITTEN/SUGGESTED/MISSING`；用户逐项审阅，不能用模型默认值静默满足required。
- feedback五态用discriminated union；空白绝不转0；`TRUE_ZERO`不能偷偷存numeric 0而丢语义。
- sensitive comment保存与model-use分开；redaction/consent后才生成model manifest；截图不OCR/入模。

### 7.2 章节编辑器

- 单章一个controller，只加载当前章与必要上下文；候选比较最多两个正文，第三按需切换。
- `contentFormat`首版为plain text/批准Markdown subset，`schemaVersion`明确；粘贴清除不允许格式、脚本/HTML按text处理。
- 5秒idle触发普通save是产品目标；新输入取消尚未发送的debounce，已发送请求用expectedRevision和AbortSignal。formal前立即flush并等待权威saved revision。
- 中文IME composition期间不触发格式/快捷键破坏；光标/selection是UI状态，不写业务表。
- 不实施段落级协同、智能merge、任意HTML、富文本插件、Web Worker diff，直到真实规模/功能触发。

### 7.3 IndexedDB draft

建议key：`accountId + taskId + objectType + objectId + serverBaseRevision + localDraftId`。record：draft schema/content format/body、base hash/revision、updatedAt、sync status、last error、migration version；不存cookie、CSRF、provider secret或download URL。

- server revision相同可恢复/重试；不同进入明确compare/keep-local/export/discard（经用户）流程，不自动覆盖。
- schema migration可重入且失败时保留原record；旧格式至少只读/导出。
- logout/account switch/task删除完成/retention到期清该scope；query cache清理不能删除未同步draft。
- quota/error可见；接近限制停止继续写并提示导出/清理，不能假保存成功。
- 共享设备风险未批准前可禁用敏感正文离线保存；端侧加密需独立密钥/恢复设计，不能以obfuscation冒充。

## 8. 正式命令与一个主CTA

页面状态由server `capabilities[] + nextAction`驱动：

- 确定性系统只有一个合法动作：该动作是唯一primary CTA。
- 多个合法低风险动作且有semantic建议：唯一primary是“审阅并选择下一步”；选择只更新local review，不mutation。用户再进入owning confirmation，D2后提交。
- `DecisionCandidatePanel`是secondary region，显示输入版本、evidence locator、contradiction、missing evidence、risk、alternative和human-review/abstain。
- model candidate不能提供`enabled=true`、final PASS/BLOCK、Cycle validity/comparability或自动执行actionId。
- formalcommand提交期间primary禁用并显示明确progress；double click复用同一idempotency key。结果未知显示“正在确认结果”并查receipt，不显示失败后新建第二结果。
- revision 409保留input，显示server/current diff或重取选项；用户重新审阅产生新commandId/key。

## 9. Responsive 与设备能力

| 宽度 | renderer/能力 | 关键实现 |
|---|---|---|
| `1440+` | wide全桌面 | 固定secondary context可用；主事实/CTA不被遮挡 |
| `1280–1439` | desktop overlay context | 全桌面能力；dialog/impact仍完整可见 |
| `768–1279` | compact workspace，通常保留桌面授权能力 | 单列/互斥full-height overlay；若完整formal preview无法安全呈现则显式要求1280×720并fail closed |
| `0–767` | mobile-readonly business | login/session/nav/read task/status/formal/trace/decision evidence；D11已生成包preview/download；D12 simple survey |

移动禁用：Bot input/action apply、candidate adoption/comparison、human-review completion、AI execution、formal mutation、release、decision、全部D10 pause/resume/terminate/archive/restore/delete、admin、D11生成配置、D12 time reconciliation。官方Web不能只用CSS隐藏：renderer layout guard与业务action capability都要拒绝，并用短时presentation ref防止resize后的陈旧提交；但viewport/User-Agent/ref不是设备证明或安全授权，非官方客户端仍只受正常身份、权限、revision、policy和业务D2约束。

边界767/768、1279/1280是行为测试点。resize过程中若进入不安全宽度：未提交form保留为local draft；modal关闭/转只读需明确提示；绝不能自动提交或丢输入。

## 10. 页面状态模板

每个feature只组合批准的通用状态，不用一张“万能空白页”代替：

- `initial-loading`：skeleton保留layout，不显示过期CTA。
- `section-loading/partial-failure`：P01四区独立，Bot故障不遮任务列表。
- `empty`：区分无对象、未introduced、无权限、无结果、筛选为空。
- `error`：errorId、保留输入、影响、recovery；不暴露技术secret。
- `offline`：只允许普通local draft；formal/execute/release/admin禁用。
- `stale/conflict`：显示旧/新revision和compare/reload；不自动merge formal facts。
- `blocked`：server reason code、severity、resolution link；合规BLOCK不可风险接受。
- `candidate/abstain/needs-human-review`：明确非正式。
- `queued/running/partial/cancelled/timeout/outcome-unknown`：保留completed output/cost。
- `unsaved/save-failed`：离开route有明确guard；浏览器关闭只能best effort，IndexedDB负责恢复。
- `not-introduced`：说明版本能力，不伪装成业务字段未填。

## 11. UI primitives、tokens 与可访问性

- `DesignSpec/tokens.json → canonical token → semantic token → local primitive → feature composition`；feature不得复制颜色/spacing/z-index常量。
- 当前只有批准的低饱和暖色主题；系统font fallback，字体/图标源与许可未确认前不下载/捆绑。
- 原生语义元素优先；Button/Link不可互换。Dialog必须有focus trap/inert、return focus、Escape/close规则；关键confirm不能靠click outside消失。
- 每页landmark/heading层级；label/description/error关联；状态同时文字/图标/颜色；focus visible；reduced motion；live region只播报重要异步变化且防刷屏。
- tables在compact转可访问card或horizontal scroll并保留header association；不能隐藏critical column而无替代。
- execution trace可pan/zoom/inspect，但有等价线性列表/键盘入口；无任意连线/保存DAG。
- DecisionCandidate证据locator可键盘打开并返回原焦点；模型建议与权威block用不同语义，不只换颜色。

## 12. 安全与隐私

- React默认escaping；批准Markdown renderer必须禁用raw HTML、allowlist link/image scheme、阻止`javascript:`/tracking、外链新窗口安全属性。模型输出一律untrusted。
- CSP/HSTS/frame/referrer/nosniff由部署批准；前端不得依赖inline script/eval。
- 不在URL、analytics、error、console、`localStorage` 或 `sessionStorage` 放正文、Prompt、评论、secret、object locator或session。唯一例外是第7.3节受控的 IndexedDB 普通草稿 repository；它仍不存 Prompt、评论、secret、locator或session，并受scope/retention/共享设备门约束。
- presigned grant短时/no-store，仅用于已批准object/method；下载文件名/media type/content disposition来自server safe metadata。
- user/admin Shell代码可共享primitive/client，但route guards、navigation和command adapter分开；admin bundle不包含user formal command shortcut。
- client telemetry使用route template、status、duration、error code等低基数字段；task/object/prompt hash不作metric label。

## 13. 性能设计

- route/feature级code splitting在bundle测量后配置；不对每个component盲目lazy。AUTH/P01/P02关键路径优先，P04/P05/Admin按introduced route加载。
- 初始shell不加载正文、全部候选、execution raw trace或admin数据；列表小projection，正文按当前对象/版本。
- query dedupe/cancel；避免waterfall：route关键查询可并行，但P01分区独立失败。
- 单章渲染；列表key稳定；大activity/cost/audit cursor分页；虚拟化仅实测DOM/内存问题后。
- image/screenshot evidence默认thumbnail/metadata，人类请求才短时加载；不进入模型/普通prefetch。
- SSE一个共享connection；事件批量精确invalidate，避免每event全页refetch。
- Lab记录build artifact、JS/CSS、route chunks、LCP/INP/CLS、long task、内存、编辑IME/滚动；Field采样/隐私/工具批准后才启用。
- 已有bootstrap bundle只作诊断基线，不是产品budget。普通交互P95≤2s、save/AI受理≤2s是目标，需代表性数据和命令证明。

## 14. 错误、恢复与降级矩阵

| 故障 | 前端行为 | 禁止行为 |
|---|---|---|
| Bot/provider | Bot区明确不可用；保留continue/pending/task list/人工路径 | 整页阻断、伪造回复、静默换模型 |
| API query部分失败 | section retry/errorId；其他独立section继续 | 用旧cache冒充current而无stale标识 |
| PG writer/quorum | formal/最新权威动作禁用；local普通draft可保留 | offline formal/发布/决定 |
| ObjectStore | 新upload/verification/processing/export generation与无法证明字节的download fail closed；PG正文/任务继续。已生成且已授权的D11包只有在ObjectStore当前响应同时证明目标version、完整性与可读字节时才可preview/download | 仅凭PG metadata、旧`lastKnownGoodRef`或health绿灯宣称上传/下载/导出成功，用不存在或不可证对象入manifest |
| SSE | 显示reconnecting，有限轮询/手动refresh | 无界快速重连、多tab风暴 |
| save 409 | 保留local，加载server compare | last-write-wins覆盖 |
| command unknown result | 查询receipt并锁定相同command上下文 | 新key盲重试产生重复事实 |
| Prompt/eval revoked | AI CTA禁用或LKG/no-AI路径；已有结果标绑定 | 继续用stale config或隐藏撤销 |
| Worker/JIT call-start或DeliveryStore异常：`AI_EXECUTION` | 只映射到owning execution资源，显示`WAITING/OUTCOME_UNKNOWN/WAITING_DIAGNOSIS`、`dataFreshness/asOf`及已保存partial/cost/receipt；新模型调用、adoption与formal progress fail closed，正常CTA被阻断时只把服务端允许的receipt/manual recovery升为sole primary | 客户端重新发provider调用、自动换模、把stream结束当result accepted；mobile启动/重试AI或执行恢复命令 |
| Worker/DeliveryStore异常：`DOCUMENT_PROCESSING` | 只映射到P03参考资料处理状态，明确保留的本地输入、PG参考metadata和先前已验证结果；新verification/processing fail closed，正常CTA被阻断时只把服务端允许的同一处理receipt/recovery升为sole primary | 把文档作业显示成AI execution、从metadata推断对象可用、重复创建处理作业；mobile启动/重试处理 |
| Worker/DeliveryStore异常：`EXPORT_GENERATION` | 只映射到D11导出请求状态，明确保留的source manifest、request receipt和先前已生成包；新generation/re-generation fail closed。先前包仅在ObjectStore当前证明目标version、完整性、授权与可读字节时可preview/download，正常CTA被阻断时仅一个服务端允许的D11 recovery可作sole primary | 把导出作业显示成AI execution、从manifest/旧LKG推断包可读、重复生成；mobile生成/重新生成/重试导出，或预览/下载当前不可证的包 |
| local quota/migration | 停止假保存，保留/导出可恢复记录 | 清全部IndexedDB/query cache一起丢草稿 |

每个降级页面统一显示`degradationMode/affectedCapabilities/dataFreshness/asOf/retryable/retryAfter/lastKnownGoodRef`、受影响范围和逐项可证的保留内容：`CURRENT`才可驱动到期正式动作；`STALE`只读并明确时间；`UNKNOWN`不显示“最新”。正常主CTA只有在仍安全且enabled时保持primary；一旦它被阻断且存在一个安全恢复动作，receipt查询、重取或compare中的唯一适用项必须升为sole primary；若没有安全恢复，则安全导航成为sole primary。其他恢复动作保持secondary，不能因503反复自动抢焦点或产生多个CTA。mobile只读仍覆盖恢复能力：不得启动或重试AI/文档处理/导出生成，唯一例外是ObjectStore当前证明可读的既有D11包可preview/download。恢复后必须GET权威资源并取得更高/相同合法revision，不能仅凭SSE reconnect、health绿灯或一次retry清除降级banner。

## 15. 测试策略

### 15.1 Unit/component

- DTO runtime guard/adapter、unknown enum/error、cursor/query key、SSE dedupe/resync、typed jobType到execution/P03参考处理/D11导出请求的唯一映射。
- reducer/form state、debounce/abort/stale response、receipt/idempotency UI、IndexedDB migration/conflict。
- capability/one CTA/DecisionCandidate分离、user/admin route隔离、mobile/compact action guard。
- primitives keyboard/focus/aria/status、Markdown/content sanitization。

### 15.2 Contract/integration

- OpenAPI generated type diff与fixture；每个endpoint success/partial/error/unknown字段。
- MSW类mock工具若选择需锁版；contract fixture来自OpenAPI，不手写第二套Schema。
- SSE disconnect/gap/duplicate/cursor expired/slow stream；command result unknown→receipt。
- IndexedDB真实browser migration/quota/account switch/task delete。

### 15.3 E2E/UIUX/visual/a11y

- UIUX scenarios 1–130每项至少一个behavior assertion；55 exact/75 representative不能当130份高保真。
- 每版关键path覆盖default、loading、empty、partial error、blocked/stale/offline、candidate/formal、completion。
- 1440×900、1280×720、批准的一个768–1279代表宽度、390×844；另测767/768、1279/1280边界。
- V1.0补Creation/DecisionCandidate/A05 exact；V1.1补P04/P05/one-cycle；V1.2补三comparability/value/N+2；A05补评测/审批/pilot/shadow/active/revoke/no-LKG/rollback。
- keyboard only、focus return、screen reader抽样、zoom/text spacing/reduced motion/contrast/非颜色状态。

### 15.4 性能与安全

- production build size/chunks/source-map政策；route navigation/save/editor/compare/large lists/SSE storm内存与P95。
- XSS/Markdown/link/download、CSRF/session expiry、object URL leakage、admin/user boundary；移动测试证明官方renderer不会误呈现/提交受限动作，direct API测试只验证正常身份/权限/revision/policy/D2不能绕过，不宣称服务器可证明物理viewport。
- offline/restart/refresh、API副本切换/SSE重连、backend部分依赖故障。
- H0 benchmark使用已确认的20文件/task、10 MB/文件、50万字符/文件、200万字符/task、300页文字PDF，以及代表性20章大纲+首批3章；按short/target/limit、cold/warm记录route chunk、LCP/INP/CLS、navigation/save/editor/large-list/SSE/内存和失败恢复。环境、浏览器/设备、网络、并发、样本/噪声、命令和阈值未批准前全部Unverified。

工具和精确命令只有进入TECH_STACK且Confirmed+Available后执行；缺失证据保持Unverified。

## 16. 分版本前端切片

| Release | 前端结果 | 横切同版门 |
|---|---|---|
| V1.0 | Auth/Shell/P01/P02/Creation Stage0/P03、references/content/candidate/Review/formal/memory/execution/export | token/primitives、API/SSE/drafts、Prompt panel/A05、mobile-readonly、a11y/perf/security/visual证据 |
| V1.1 | Operation Stage0、P04 packaging/release/feedback、P05 analysis/continue/human decision、每ended Cycle time reconciliation | V1.0 regression、privacy/evidence/stale correction、one-cycle outcome、P04/P05 exact |
| V1.2 | decision→plan→P03/P04、N/N+1 comparison/value、N+2 entry | V1.0/1.1 regression、non-causal copy、three comparability、simple mobile survey |

后一版不能把前版creation/edit/Review/formal降为只读；later feature未introduced不显示成“填写后可解锁”。

前端物理manifest必须消费[数据与接口合同设计](V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md)的精确Public目录集合：H0仅生成/调用`PUB-001–PUB-021,PUB-025–PUB-066,PUB-092–PUB-107`；H1累计增加`PUB-022–PUB-024,PUB-067–PUB-085,PUB-089`；H2累计增加`PUB-086–PUB-088,PUB-090–PUB-091`。每个范围须在manifest展开完整method/path并绑定route/action/capability/negative deep-link test；未到期endpoint即使后端意外可达也不生成client、不注册route、不显示action。该集合仍Proposed/Unverified，V2金融route/object/action全部deny。

## 17. 实施前审批与验证门

1. UIUX roadmap overlay、route/action/capability和每版exact evidence计划最终批准。
2. Router/query/form/IndexedDB/OpenAPI/E2E/a11y/visual候选精确锁版、许可证/安全/bundle/命令批准。
3. REST/SSE/error/receipt/idempotency/OpenAPI、官方Web responsive conformance与presentation-ref陈旧提交合同批准；不把它写成设备attestation。
4. contentFormat/Markdown subset、draft schema/migration/quota/shared-device策略批准。
5. CSP/CSRF/session/download/telemetry/privacy设计和安全测试批准。
6. 代表性数据、浏览器、设备、网络、performance命令/阈值批准。

## 18. 本文验证边界

本文只新增评审稿，未修改Web source/manifest/lock，未运行产品build/unit/E2E/visual/a11y/performance/security测试。所有业务前端能力仍为`NotYetImplemented/Unverified`；回退只删除本文。
