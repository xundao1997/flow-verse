# FlowVerse（流界）

FlowVerse V1 是一个面向长篇小说创作与真实运营闭环的多模型、多 Agent 工作台。当前仓库完成的是 V1 的非业务架构版：三个独立代码服务、运行与质量基线、真实依赖诊断和本地原生测试部署入口已经具备；认证、创作、发布、反馈、分析等正式业务尚未实现。

## 当前可运行架构

```mermaid
flowchart LR
    Browser["浏览器"] -->|"GET /api/v1/system/chain"| Web["Web · React/Vite · 5173/8080"]
    Web --> API["API · FastAPI · 8000"]
    API -->|"GET /internal/v1/system/status\n2 秒超时 / 0 重试"| Worker["Worker · FastAPI · 8001"]
    API --> ApiDb["PostgreSQL"]
    Worker --> WorkerDb["PostgreSQL"]
```

Web 提供简体中文架构检查页；API 聚合自身和 Worker 状态；API、Worker 分别执行有界 PostgreSQL 探针。未配置数据库时，页面仍能打开并如实显示降级，不会伪造成功。

## 目录与包

| 路径 | 所有权与内容 |
|---|---|
| `services/web` | 检查页、Vite 开发代理、Vitest 测试、Nginx 生产镜像 |
| `services/api` | 公共健康/链路接口、API PostgreSQL 探针、Worker 客户端、Alembic 空基线 |
| `services/worker` | 常驻内部状态服务、Worker PostgreSQL 探针、兼容的一次性 `--check` |
| `scripts` | 本地原生启动、模块边界/循环依赖检查及其自测 |
| `deploy/local` | 当前本地测试部署入口和使用说明，不使用 Docker |
| `docs/product` / `docs/uiux` | 已批准的 PRD v1.1 产品与 UIUX 摘要 |
| `docs/engineering` | 技术栈、架构、可靠性、性能、编码流程和技术债登记 |
| `docs/decisions` | ADR 决策记录；ADR-0006 是当前本地测试部署决策 |

业务模块边界已经声明但没有业务实现：API 拥有身份权限、任务生命周期、创作资料、创作内容、Review/合规、发布/Cycle、反馈/决策和治理运维；Worker 独立拥有 AI execution。服务之间禁止直接导入源码，模块跨边界只能通过 `public` 入口。

### 为什么有 `services/api/src/flowverse_api`

`services/api` 是可独立安装、测试和部署的服务工程；`src` 是 Python 的源码隔离层；`flowverse_api` 是安装后稳定的 Python 导入命名空间；它里面的 `api` 才是 FastAPI HTTP 适配层。这个标准 `src layout` 可以阻止项目根目录被偶然导入，确保本地测试与安装/容器运行使用同一套导入行为。Worker 使用同样结构和独立命名空间 `flowverse_worker`。

## 主要版本

| 区域 | 版本 |
|---|---|
| Python / uv | CPython 3.13.14 / uv 0.11.28 |
| API 与 Worker | FastAPI 0.139.0 / Uvicorn 0.51.0 |
| 数据访问 | PostgreSQL 18.4 目标；SQLAlchemy 2.0.51 / Alembic 1.18.5 / psycopg 3.3.4 |
| Web 运行时 | Node.js 24.17.0 / pnpm 11.10.0 |
| Web | React 19.2.7 / Vite 8.1.4 / TypeScript 5.9.3 |
| Web 质量 | ESLint 10.6.0 / Prettier 3.9.5 / Vitest 4.1.9 |
| Python 质量 | Ruff 0.15.20 / Pyright 1.1.411 / pytest 9.1.1 |
| 可观测性 | structlog 26.1.0 / OpenTelemetry 1.43.0（当前无 exporter） |

精确直接依赖和命令状态以 [`docs/engineering/TECH_STACK.md`](docs/engineering/TECH_STACK.md) 为准。

## 本地准备

本地运行不使用 Docker。需要提前安装：

- Python 3.13.14 与 uv 0.11.28；
- Node.js 24.17.0（必须使用该版本）和 Corepack；
- PostgreSQL 18.4，或者一个兼容且由你独立提供的 PostgreSQL 实例。

安装锁定依赖：

```powershell
uv sync --project services/api --python 3.13.14
uv sync --project services/worker --python 3.13.14
corepack pnpm@11.10.0 --dir services/web install --frozen-lockfile
```

复制环境模板并只修改本地值：

```powershell
Copy-Item .env.example .env
```

必须把 `.env` 中的 `FLOWVERSE_DATABASE_URL` 改为真实本地连接。脚本不会打印环境值，也不会覆盖当前进程中已经设置的变量。当前架构版不需要 Redis、消息队列、对象存储或 AI Provider SDK。

## 启动和验证

先检查运行时：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1 preflight
```

一条命令启动三服务：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1
```

脚本会隐藏启动 API 和 Worker、等待二者存活，再以前台方式启动 Web。按 `Ctrl+C` 退出时只清理本次启动的子进程。打开：

- 检查页：`http://127.0.0.1:5173/`
- 完整链路：`http://127.0.0.1:8000/api/v1/system/chain`
- API 存活：`http://127.0.0.1:8000/health/live`
- API 就绪：`http://127.0.0.1:8000/health/ready`
- Worker 存活：`http://127.0.0.1:8001/health/live`
- Worker 内部状态：`http://127.0.0.1:8001/internal/v1/system/status`

也可以向 `deploy/local/start.ps1` 传入 `api`、`worker`、`web`、`worker-check` 或 `all`。只有 API、Worker 和双方 PostgreSQL 探针都可用时，完整链路返回 200；缺少数据库配置时返回 503 是预期、真实的降级结果。

## 质量检查

仓库定义了 Web lint/format/typecheck/test/build、两个 Python 服务的 Ruff/Pyright/pytest，以及架构检查与架构检查器自测。精确命令都登记在技术栈文档中。最小架构检查为：

```powershell
python scripts/check_architecture.py
python -m unittest scripts.test_check_architecture
```

## 部署边界

当前唯一部署入口是 [`deploy/local/start.ps1`](deploy/local/start.ps1)，只用于 Windows 本地架构测试。它复用 `scripts/start-local.ps1` 的服务编排，不复制第二套启动逻辑，也不使用 Docker、云效或其他云端服务。

仓库目前没有选定 CI/CD、测试服务器或生产部署目标。三个服务的 Dockerfile 只作为未激活的独立打包入口保留，不属于当前本地启动链路。未来需要云端、测试环境或生产发布时，必须重新确认目标并新增 ADR。

## 架构版之外

以下内容没有被“架构版完成”伪装为已实现：正式认证授权、任务/创作/Review/Cycle 业务、业务表结构、AI Provider 与任务队列、对象存储、Redis、生产监控 exporter、备份恢复、CI/CD、测试服务器、生产部署和产品验收。实施这些内容前，继续遵循批准范围和 [`docs/engineering/AI_CODING_WORKFLOW.md`](docs/engineering/AI_CODING_WORKFLOW.md)。
