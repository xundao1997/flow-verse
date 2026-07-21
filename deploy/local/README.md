# FlowVerse 本地测试部署

该目录是当前唯一的部署入口，用于在 Windows 本机原生启动架构测试环境。它不使用 Docker，也不连接云效或其他云端控制面。

## 准备

在仓库根目录安装锁定依赖：

```powershell
uv sync --project services/api --python 3.13.14
uv sync --project services/worker --python 3.13.14
corepack pnpm@11.10.0 --dir services/web install --frozen-lockfile
Copy-Item .env.example .env
```

把 `.env` 中的 `FLOWVERSE_DATABASE_URL` 改为本地 PostgreSQL 连接。没有 PostgreSQL 时三个代码服务仍可启动，但检查页会如实显示降级状态。

## 启动

默认启动 Web、API、Worker：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1
```

Web 在前台运行；API、Worker 隐藏运行并将日志写到命令输出提示的临时目录。按 `Ctrl+C` 退出后，本次启动的 API、Worker 子进程会被清理。

先检查运行时但不启动服务：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1 preflight
```

也可以传入 `api`、`worker`、`worker-check`、`web` 或 `all`。实际服务编排由 `scripts/start-local.ps1` 统一维护，本文件只提供稳定的本地测试部署入口，避免复制两套启动逻辑。

## 验证地址

- 检查页：`http://127.0.0.1:5173/`
- 完整链路：`http://127.0.0.1:8000/api/v1/system/chain`
- API 存活：`http://127.0.0.1:8000/health/live`
- Worker 存活：`http://127.0.0.1:8001/health/live`

只有 API、Worker 以及双方 PostgreSQL 探针全部可用时，完整链路才返回 200；未配置数据库时返回 503 `configuration` 是预期结果。
