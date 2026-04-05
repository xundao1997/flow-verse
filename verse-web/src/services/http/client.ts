import { env } from '@/config/env';

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly payload?: unknown,
  ) {
    super(message);
    this.name = 'ApiRequestError';
  }
}

export type RequestOptions = Omit<RequestInit, 'body'> & {
  baseUrl?: string;
  body?: BodyInit | Record<string, unknown>;
  query?: Record<string, string | number | boolean | undefined>;
  timeoutMs?: number;
};

function buildUrl(path: string, query?: RequestOptions['query'], baseUrl = env.apiBaseUrl) {
  const target = new URL(path, baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`);

  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined) {
        target.searchParams.set(key, String(value));
      }
    });
  }

  return target.toString();
}

function normalizeBody(body: RequestOptions['body']) {
  if (!body || body instanceof FormData || typeof body === 'string') {
    return body;
  }

  return JSON.stringify(body);
}

export async function request<TResponse>(path: string, options: RequestOptions = {}): Promise<TResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), options.timeoutMs ?? env.requestTimeoutMs);

  try {
    const response = await fetch(buildUrl(path, options.query, options.baseUrl), {
      ...options,
      body: normalizeBody(options.body),
      headers: {
        Accept: 'application/json',
        ...(options.body && !(options.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
      signal: controller.signal,
    });

    const contentType = response.headers.get('content-type') || '';
    const payload = contentType.includes('application/json') ? await response.json() : await response.text();

    if (!response.ok) {
      throw new ApiRequestError(`Request failed with status ${response.status}`, response.status, payload);
    }

    return payload as TResponse;
  } finally {
    window.clearTimeout(timeoutId);
  }
}
