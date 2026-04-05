/* eslint-disable no-var */

type RuntimeEnv = {
  appName: string;
  apiBaseUrl: string;
  requestTimeoutMs: number;
};

type RuntimeEnvSource = Partial<Record<'VITE_APP_NAME' | 'VITE_API_BASE_URL' | 'VITE_REQUEST_TIMEOUT_MS', string>>;

declare global {
  var __APP_ENV__: RuntimeEnvSource | undefined;
}

function readNumber(value: string | undefined, fallback: number) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function readRuntimeEnv(): RuntimeEnvSource {
  if (typeof globalThis !== 'undefined' && globalThis.__APP_ENV__) {
    return globalThis.__APP_ENV__;
  }

  if (typeof process !== 'undefined') {
    return process.env as RuntimeEnvSource;
  }

  return {};
}

const runtimeSource = readRuntimeEnv();

export const env: RuntimeEnv = Object.freeze({
  appName: runtimeSource.VITE_APP_NAME?.trim() || 'Verse Web',
  apiBaseUrl: runtimeSource.VITE_API_BASE_URL?.trim() || 'http://localhost:8000/api/v1',
  requestTimeoutMs: readNumber(runtimeSource.VITE_REQUEST_TIMEOUT_MS, 8000),
});
