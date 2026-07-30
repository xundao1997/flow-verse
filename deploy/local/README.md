# FlowVerse 本地测试部署

该目录是 Windows 本机应用测试部署入口，用于原生启动架构测试环境。它不使用 Docker，也不连接云效或其他云端控制面；服务器中间件由独立的 `deploy/server/middleware` 入口管理。

## 准备

在仓库根目录安装锁定依赖：

```powershell
uv sync --project services/api --python 3.13.14
uv sync --project services/worker --python 3.13.14
corepack pnpm@11.10.0 --dir services/web install --frozen-lockfile
Copy-Item .env.example .env
```

把 `.env` 中的 `FLOWVERSE_DATABASE_URL` 改为本地 PostgreSQL 连接。没有 PostgreSQL 时三个代码服务仍可启动，但检查页会如实显示降级状态。

### 使用服务器中间件进行本地开发

服务器中间件端口默认只监听服务器 `127.0.0.1`，不要为了本地开发把 PostgreSQL、Redis 或 MinIO 直接暴露到公网。仓库提供一个本地 SSH 隧道入口；请在第一个 PowerShell 窗口运行，并将示例主机名和 SSH 用户替换为你的服务器信息：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start-middleware-tunnel.ps1 `
  -Server "your-server.example.com" `
  -SshUser "your-ssh-user"
```

默认本地映射如下，所有监听仍限定为本机 `127.0.0.1`：

| 中间件 | 本地地址 | 服务器私有地址 |
|---|---|---|
| PostgreSQL | `127.0.0.1:15432` | `127.0.0.1:5432` |
| Redis | `127.0.0.1:16379` | `127.0.0.1:6379` |
| MinIO API | `127.0.0.1:19000` | `127.0.0.1:9000` |
| MinIO Console | `http://127.0.0.1:19001` | `127.0.0.1:9001` |

使用 SSH 私钥时增加 `-IdentityFile "C:\path\to\private-key"`。本地端口被占用时，可以通过 `-PostgresLocalPort`、`-RedisLocalPort`、`-MinioApiLocalPort`、`-MinioConsoleLocalPort` 分别调整。脚本启用 `ExitOnForwardFailure`、10 秒连接超时和 SSH keepalive；连接失败会返回非零退出码，按 `Ctrl+C` 会关闭全部转发。

在第二个 PowerShell 窗口运行安全配置入口。它会分别提示输入 PostgreSQL、Redis 和 MinIO 凭据，不回显密码，并把 URL 转义后的值写入已被 Git 忽略的根 `.env`；写入后立即执行三项认证检查：

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File deploy/local/configure-middleware.ps1
```

配置完成后可随时重复认证检查而不再次输入：

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File deploy/local/start.ps1 middleware-check
```

成功结果要求 PostgreSQL `SELECT 1`、Redis `AUTH`/`PING` 和 MinIO 签名只读 `ListBuckets` 全部返回 `ready`。检查不会创建表、Redis 键或 MinIO Bucket，也不会打印密码、响应正文或 Bucket 名称。该命令只证明本地诊断连接，不能视为 Redis 缓存/队列或 MinIO 业务对象契约已经实现。MinIO root 凭据仅用于此架构诊断；正式应用必须另行批准并创建最小权限账号。

只检查本地参数、端口和 OpenSSH 是否可用而不连接服务器：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/local/start-middleware-tunnel.ps1 `
  -Server "your-server.example.com" `
  -SshUser "your-ssh-user" `
  -ValidateOnly
```

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

也可以传入 `api`、`worker`、`worker-check`、`middleware-check`、`web` 或 `all`。实际服务编排由 `scripts/start-local.ps1` 统一维护，本文件只提供稳定的本地测试部署入口，避免复制两套启动逻辑。

## 验证地址

- 检查页：`http://127.0.0.1:5173/`
- 完整链路：`http://127.0.0.1:8000/api/v1/system/chain`
- API 存活：`http://127.0.0.1:8000/health/live`
- Worker 存活：`http://127.0.0.1:8001/health/live`

只有 API、Worker 以及双方 PostgreSQL 探针全部可用时，完整链路才返回 200；未配置数据库时返回 503 `configuration` 是预期结果。
