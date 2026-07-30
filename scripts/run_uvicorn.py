from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import Callable, Sequence

import uvicorn

LoopFactory = Callable[[], asyncio.AbstractEventLoop]


def resolve_loop(platform: str) -> str | LoopFactory:
    if platform == "win32":
        return asyncio.SelectorEventLoop
    return "auto"


def main(argv: Sequence[str] | None = None, *, platform: str = sys.platform) -> int:
    parser = argparse.ArgumentParser(description="Run a FlowVerse ASGI service.")
    parser.add_argument("app")
    parser.add_argument("--app-dir", default=".")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args(argv)

    uvicorn.run(
        args.app,
        app_dir=args.app_dir,
        host=args.host,
        port=args.port,
        loop=resolve_loop(platform),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
