import { ApiRequestError, request } from '@/services/http/client';

type MockResponse = {
  ok: boolean;
  status: number;
  headers: {
    get: (key: string) => string | null;
  };
  json: () => Promise<unknown>;
  text: () => Promise<string>;
};

function createJsonResponse(status: number, payload: unknown): MockResponse {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: {
      get: (key: string) => (key.toLowerCase() === 'content-type' ? 'application/json' : null),
    },
    json: async () => payload,
    text: async () => JSON.stringify(payload),
  };
}

afterEach(() => {
  jest.restoreAllMocks();
});

it('resolves JSON responses through the request client', async () => {
  const fetchMock = jest.fn().mockResolvedValue(createJsonResponse(200, { status: 'ok' }));
  Object.defineProperty(globalThis, 'fetch', {
    value: fetchMock,
    writable: true,
  });

  const response = await request<{ status: string }>('/health', {
    baseUrl: 'https://example.com',
  });

  expect(response.status).toBe('ok');
  expect(fetchMock).toHaveBeenCalledWith(
    'https://example.com/health',
    expect.objectContaining({
      headers: expect.objectContaining({
        Accept: 'application/json',
      }),
    }),
  );
});

it('throws a typed request error on non-success responses', async () => {
  const fetchMock = jest.fn().mockResolvedValue(createJsonResponse(500, { message: 'Nope' }));
  Object.defineProperty(globalThis, 'fetch', {
    value: fetchMock,
    writable: true,
  });

  await expect(
    request('/health', {
      baseUrl: 'https://example.com',
    }),
  ).rejects.toBeInstanceOf(ApiRequestError);
});
