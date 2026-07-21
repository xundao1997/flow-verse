export const serviceReasons = [
  "ready",
  "configuration",
  "timeout",
  "probe_failure",
  "connection",
  "invalid_response",
] as const;

export type ServiceReason = (typeof serviceReasons)[number];

export interface ServiceState {
  status: "ready" | "unavailable";
  reason: ServiceReason;
}

export interface ChainResponse {
  status: "ready" | "degraded";
  services: {
    api: ServiceState;
    worker: ServiceState;
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function parseServiceState(value: unknown): ServiceState | null {
  if (!isRecord(value)) {
    return null;
  }

  const status = value.status;
  const reason = value.reason;
  if (
    (status !== "ready" && status !== "unavailable") ||
    typeof reason !== "string" ||
    !serviceReasons.includes(reason as ServiceReason)
  ) {
    return null;
  }

  if ((status === "ready") !== (reason === "ready")) {
    return null;
  }

  return { status, reason: reason as ServiceReason };
}

export function parseChainResponse(value: unknown): ChainResponse | null {
  if (
    !isRecord(value) ||
    (value.status !== "ready" && value.status !== "degraded")
  ) {
    return null;
  }

  if (!isRecord(value.services)) {
    return null;
  }

  const api = parseServiceState(value.services.api);
  const worker = parseServiceState(value.services.worker);
  if (api === null || worker === null) {
    return null;
  }

  const allReady = api.status === "ready" && worker.status === "ready";
  if ((value.status === "ready") !== allReady) {
    return null;
  }

  return { status: value.status, services: { api, worker } };
}

export const reasonLabels: Record<ServiceReason, string> = {
  ready: "已连通",
  configuration: "缺少 PostgreSQL 配置",
  timeout: "依赖检查超时",
  probe_failure: "依赖检查失败",
  connection: "服务连接失败",
  invalid_response: "服务响应无法识别",
};
