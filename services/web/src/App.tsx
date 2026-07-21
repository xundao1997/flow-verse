import { useCallback, useEffect, useRef, useState } from "react";

import {
  parseChainResponse,
  reasonLabels,
  type ChainResponse,
  type ServiceReason,
} from "./chain";

type CheckState =
  | { phase: "loading" }
  | { phase: "complete"; response: ChainResponse; checkedAt: Date }
  | { phase: "error"; message: string };

interface ServiceCardProps {
  description: string;
  name: string;
  reason: ServiceReason | "checking" | "unknown";
  status: "ready" | "unavailable" | "checking";
}

const serviceCopy: Record<ServiceCardProps["status"], string> = {
  ready: "可用",
  unavailable: "不可用",
  checking: "检查中",
};

function ServiceCard({ description, name, reason, status }: ServiceCardProps) {
  const reasonText =
    reason === "checking"
      ? "正在获取当前状态"
      : reason === "unknown"
        ? "未能获取当前状态"
        : reasonLabels[reason];

  return (
    <article className={`service-card service-card--${status}`}>
      <div className="service-card__heading">
        <h2>{name}</h2>
        <span className="status-label">
          <span className="status-dot" aria-hidden="true" />
          {serviceCopy[status]}
        </span>
      </div>
      <p>{description}</p>
      <p className="service-card__reason">{reasonText}</p>
    </article>
  );
}

function errorMessage(error: unknown): string {
  if (error instanceof DOMException && error.name === "AbortError") {
    return "检查已取消。";
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "发生未知错误。";
}

export function App() {
  const [state, setState] = useState<CheckState>({ phase: "loading" });
  const activeRequest = useRef<AbortController | null>(null);

  const checkChain = useCallback(async () => {
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    setState({ phase: "loading" });

    try {
      const response = await fetch("/api/v1/system/chain", {
        headers: { Accept: "application/json" },
        signal: controller.signal,
      });
      if (response.status !== 200 && response.status !== 503) {
        throw new Error(`服务返回了未预期的状态码 ${response.status}。`);
      }

      const payload: unknown = await response.json();
      const chain = parseChainResponse(payload);
      if (chain === null) {
        throw new Error("服务返回的数据格式不完整。");
      }

      if (!controller.signal.aborted) {
        setState({ phase: "complete", response: chain, checkedAt: new Date() });
      }
    } catch (error: unknown) {
      if (!controller.signal.aborted) {
        setState({ phase: "error", message: errorMessage(error) });
      }
    }
  }, []);

  useEffect(() => {
    void checkChain();
    return () => activeRequest.current?.abort();
  }, [checkChain]);

  const isLoading = state.phase === "loading";
  const isReady =
    state.phase === "complete" && state.response.status === "ready";
  const api = state.phase === "complete" ? state.response.services.api : null;
  const worker =
    state.phase === "complete" ? state.response.services.worker : null;

  return (
    <main className="page-shell">
      <header className="brand-bar">
        <a className="brand" href="/" aria-label="流界 FlowVerse 架构检查页">
          <span className="brand__mark" aria-hidden="true">
            流
          </span>
          <span>
            <strong>流界</strong>
            <small>FlowVerse</small>
          </span>
        </a>
        <span className="environment-label">架构验证环境</span>
      </header>

      <section className="check-panel" aria-labelledby="page-title">
        <div className="check-panel__intro">
          <p className="eyebrow">DEPLOYMENT CHECK</p>
          <h1 id="page-title">架构链路检查</h1>
          <p className="lead">
            验证浏览器、API、Worker 与各自 PostgreSQL 依赖是否已经正确串联。
          </p>
        </div>

        <div className="summary" aria-live="polite" aria-atomic="true">
          <span
            className={`summary__icon ${isReady ? "summary__icon--ready" : ""}`}
            aria-hidden="true"
          >
            {isLoading ? "…" : isReady ? "✓" : "!"}
          </span>
          <div>
            <strong>
              {isLoading
                ? "正在检查架构链路"
                : isReady
                  ? "架构链路已全部连通"
                  : state.phase === "error"
                    ? "暂时无法完成检查"
                    : "架构链路部分不可用"}
            </strong>
            <p>
              {state.phase === "error"
                ? `${state.message} 页面数据未被修改，请确认服务启动后重试。`
                : isLoading
                  ? "正在等待各服务返回真实依赖状态。"
                  : isReady
                    ? "三个代码服务与 PostgreSQL 依赖均已通过本次检查。"
                    : "页面仍可访问；请根据下方原因恢复依赖后重新检查。"}
            </p>
          </div>
        </div>

        <div className="service-grid" aria-label="服务状态">
          <ServiceCard
            name="Web 前端"
            description="当前检查页面与静态资源"
            status="ready"
            reason="ready"
          />
          <ServiceCard
            name="API 服务"
            description="公共诊断接口与 API 数据库连接"
            status={isLoading ? "checking" : (api?.status ?? "unavailable")}
            reason={isLoading ? "checking" : (api?.reason ?? "unknown")}
          />
          <ServiceCard
            name="Worker 服务"
            description="内部诊断接口与 Worker 数据库连接"
            status={isLoading ? "checking" : (worker?.status ?? "unavailable")}
            reason={isLoading ? "checking" : (worker?.reason ?? "unknown")}
          />
        </div>

        <footer className="check-panel__footer">
          <p>
            {state.phase === "complete"
              ? `最近检查：${state.checkedAt.toLocaleString("zh-CN", { hour12: false })}`
              : "检查不会自动轮询。"}
          </p>
          <button
            type="button"
            onClick={() => void checkChain()}
            disabled={isLoading}
          >
            {isLoading ? "检查中…" : "重新检查"}
          </button>
        </footer>
      </section>

      <p className="page-note">此页面只用于部署连通性验证，不写入业务数据。</p>
    </main>
  );
}
