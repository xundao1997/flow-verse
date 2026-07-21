from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_architecture


class ArchitectureCheckTests(unittest.TestCase):
    def check_fixture(self, relative_file: str, source: str) -> tuple[list[str], int]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = root / "services" / "api" / "src"
            modules_root = source_root / "flowverse_api" / "modules"
            for module in ("consumer", "provider"):
                (modules_root / module).mkdir(parents=True)
            (modules_root / "provider" / "private.py").write_text(
                "value = 1\n", encoding="utf-8"
            )

            target = source_root / relative_file
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source, encoding="utf-8")

            service = check_architecture.Service(
                name="api",
                namespace="flowverse_api",
                source_root=source_root,
                modules_root=modules_root,
            )
            with (
                patch.object(check_architecture, "REPOSITORY_ROOT", root),
                patch.object(check_architecture, "SERVICES", (service,)),
            ):
                _, violations, edge_count = check_architecture.check_service(service)
            return violations, edge_count

    def test_relative_private_module_import_is_rejected(self) -> None:
        violations, edge_count = self.check_fixture(
            "flowverse_api/modules/consumer/use.py",
            "from ..provider.private import value\n",
        )

        self.assertEqual(edge_count, 1)
        self.assertTrue(any("private module import" in item for item in violations))

    def test_application_layer_private_module_import_is_rejected(self) -> None:
        violations, edge_count = self.check_fixture(
            "flowverse_api/api/route.py",
            "from flowverse_api.modules.provider.private import value\n",
        )

        self.assertEqual(edge_count, 0)
        self.assertTrue(any("private module import" in item for item in violations))

    def test_from_package_private_alias_is_rejected(self) -> None:
        violations, edge_count = self.check_fixture(
            "flowverse_api/modules/consumer/use.py",
            "from flowverse_api.modules.provider import private\n",
        )

        self.assertEqual(edge_count, 1)
        self.assertTrue(any("private module import" in item for item in violations))

    def test_from_modules_provider_alias_tracks_dependency(self) -> None:
        violations, edge_count = self.check_fixture(
            "flowverse_api/modules/consumer/use.py",
            "from flowverse_api.modules import provider\n",
        )

        self.assertEqual(violations, [])
        self.assertEqual(edge_count, 1)

    def test_public_module_import_is_allowed(self) -> None:
        violations, edge_count = self.check_fixture(
            "flowverse_api/modules/consumer/use.py",
            "from ..provider.public import value\n",
        )

        self.assertEqual(violations, [])
        self.assertEqual(edge_count, 1)


if __name__ == "__main__":
    unittest.main()
