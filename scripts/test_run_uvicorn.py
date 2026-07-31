from __future__ import annotations

import asyncio
import unittest
from unittest.mock import patch

from scripts.run_uvicorn import main, resolve_loop


class RunUvicornTests(unittest.TestCase):
    def test_windows_uses_selector_event_loop(self) -> None:
        self.assertIs(resolve_loop("win32"), asyncio.SelectorEventLoop)

    def test_non_windows_keeps_uvicorn_default(self) -> None:
        self.assertEqual(resolve_loop("linux"), "auto")

    @patch("scripts.run_uvicorn.uvicorn.run")
    def test_main_forwards_service_arguments(self, run: unittest.mock.Mock) -> None:
        result = main(
            [
                "package.app:app",
                "--app-dir",
                "src",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            platform="win32",
        )

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            "package.app:app",
            app_dir="src",
            host="127.0.0.1",
            port=8000,
            loop=asyncio.SelectorEventLoop,
        )


if __name__ == "__main__":
    unittest.main()
