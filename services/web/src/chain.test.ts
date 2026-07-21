import { describe, expect, it } from "vitest";

import { parseChainResponse } from "./chain";

describe("parseChainResponse", () => {
  it("accepts a ready architecture chain", () => {
    expect(
      parseChainResponse({
        status: "ready",
        services: {
          api: { status: "ready", reason: "ready" },
          worker: { status: "ready", reason: "ready" },
        },
      }),
    ).toEqual({
      status: "ready",
      services: {
        api: { status: "ready", reason: "ready" },
        worker: { status: "ready", reason: "ready" },
      },
    });
  });

  it("accepts a truthful degraded chain", () => {
    expect(
      parseChainResponse({
        status: "degraded",
        services: {
          api: { status: "unavailable", reason: "configuration" },
          worker: { status: "unavailable", reason: "connection" },
        },
      }),
    )?.toEqual({
      status: "degraded",
      services: {
        api: { status: "unavailable", reason: "configuration" },
        worker: { status: "unavailable", reason: "connection" },
      },
    });
  });

  it("rejects inconsistent and incomplete payloads", () => {
    expect(
      parseChainResponse({
        status: "ready",
        services: {
          api: { status: "unavailable", reason: "configuration" },
          worker: { status: "ready", reason: "ready" },
        },
      }),
    ).toBeNull();
    expect(parseChainResponse({ status: "degraded", services: {} })).toBeNull();
  });
});
