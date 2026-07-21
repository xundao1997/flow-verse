#!/usr/bin/env python3
"""Validate service isolation, public module imports, and acyclic module graphs."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Service:
    name: str
    namespace: str
    source_root: Path
    modules_root: Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SERVICES = (
    Service(
        name="api",
        namespace="flowverse_api",
        source_root=REPOSITORY_ROOT / "services" / "api" / "src",
        modules_root=REPOSITORY_ROOT
        / "services"
        / "api"
        / "src"
        / "flowverse_api"
        / "modules",
    ),
    Service(
        name="worker",
        namespace="flowverse_worker",
        source_root=REPOSITORY_ROOT / "services" / "worker" / "src",
        modules_root=REPOSITORY_ROOT
        / "services"
        / "worker"
        / "src"
        / "flowverse_worker"
        / "modules",
    ),
)
EXPECTED_MODULES = {
    "identity_access",
    "task_lifecycle",
    "creative_reference",
    "creative_content",
    "review_compliance",
    "ai_execution",
    "release_cycle",
    "feedback_decision",
    "governance_ops",
}


def source_module_name(source: Path, source_root: Path) -> str:
    relative = source.relative_to(source_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def resolve_from_import(
    *,
    source: Path,
    source_root: Path,
    module: str | None,
    level: int,
) -> str | None:
    if level == 0:
        return module

    current_module = source_module_name(source, source_root)
    package_parts = current_module.split(".")
    if source.name != "__init__.py":
        package_parts.pop()
    parent_count = level - 1
    if parent_count > len(package_parts):
        return module
    if parent_count:
        package_parts = package_parts[:-parent_count]
    if module:
        package_parts.extend(module.split("."))
    return ".".join(package_parts) or None


def import_target_exists(target: str, source_root: Path) -> bool:
    path = source_root.joinpath(*target.split("."))
    return path.is_dir() or path.with_suffix(".py").is_file()


def imported_names(source: Path, source_root: Path) -> tuple[tuple[int, str], ...]:
    tree = ast.parse(source.read_text(encoding="utf-8"), source)
    names: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            target = resolve_from_import(
                source=source,
                source_root=source_root,
                module=node.module,
                level=node.level,
            )
            if target:
                names.append((node.lineno, target))
                names.extend(
                    (node.lineno, candidate)
                    for alias in node.names
                    if alias.name != "*"
                    and import_target_exists(
                        candidate := f"{target}.{alias.name}", source_root
                    )
                )
    return tuple(names)


def cycle_key(nodes: list[str]) -> tuple[str, ...]:
    body = nodes[:-1]
    rotation = min(tuple(body[index:] + body[:index]) for index in range(len(body)))
    return (*rotation, rotation[0])


def cycles(graph: dict[str, set[str]]) -> tuple[tuple[str, ...], ...]:
    state = {module: 0 for module in graph}
    stack: list[str] = []
    found: set[tuple[str, ...]] = set()

    def visit(module: str) -> None:
        state[module] = 1
        stack.append(module)
        for dependency in sorted(graph[module]):
            if state[dependency] == 0:
                visit(dependency)
            elif state[dependency] == 1:
                start = stack.index(dependency)
                found.add(cycle_key([*stack[start:], dependency]))
        stack.pop()
        state[module] = 2

    for module in sorted(graph):
        if state[module] == 0:
            visit(module)
    return tuple(sorted(found))


def check_service(service: Service) -> tuple[set[str], list[str], int]:
    if not service.modules_root.is_dir():
        return set(), [f"{service.name}: missing module root {service.modules_root}"], 0

    modules = {
        path.name
        for path in service.modules_root.iterdir()
        if path.is_dir() and not path.name.startswith("_")
    }
    graph = {module: set() for module in modules}
    violations: list[str] = []
    other_namespaces = {item.namespace for item in SERVICES if item != service}

    for source in sorted(service.source_root.rglob("*.py")):
        if "__pycache__" in source.parts:
            continue
        relative = source.relative_to(REPOSITORY_ROOT)
        try:
            imports = imported_names(source, service.source_root)
        except (OSError, UnicodeError, SyntaxError) as error:
            violations.append(f"{relative}: cannot parse source: {error}")
            continue

        owner = None
        if service.modules_root in source.parents:
            owner = source.relative_to(service.modules_root).parts[0]
            if owner not in modules:
                owner = None

        for line, target in imports:
            if any(target == namespace or target.startswith(f"{namespace}.") for namespace in other_namespaces):
                violations.append(
                    f"{relative}:{line}: direct cross-service import '{target}' is forbidden"
                )
            prefix = f"{service.namespace}.modules."
            if not target.startswith(prefix):
                continue
            parts = target.removeprefix(prefix).split(".")
            provider = parts[0]
            tail = tuple(parts[1:])
            if provider not in modules or provider == owner:
                continue
            if owner is not None:
                graph[owner].add(provider)
            if tail not in ((), ("public",)):
                violations.append(
                    f"{relative}:{line}: private module import '{target}'; "
                    f"use '{prefix}{provider}' or '{prefix}{provider}.public'"
                )

    violations.extend(
        f"{service.name}: dependency cycle: {' -> '.join(cycle)}"
        for cycle in cycles(graph)
    )
    return modules, violations, sum(len(dependencies) for dependencies in graph.values())


def main() -> int:
    discovered: set[str] = set()
    violations: list[str] = []
    edge_count = 0
    for service in SERVICES:
        modules, service_violations, edges = check_service(service)
        duplicates = discovered.intersection(modules)
        if duplicates:
            violations.append(
                f"duplicate module ownership: {', '.join(sorted(duplicates))}"
            )
        discovered.update(modules)
        violations.extend(service_violations)
        edge_count += edges

    missing = EXPECTED_MODULES - discovered
    unexpected = discovered - EXPECTED_MODULES
    if missing:
        violations.append(f"missing module ownership: {', '.join(sorted(missing))}")
    if unexpected:
        violations.append(f"unexpected modules: {', '.join(sorted(unexpected))}")

    if violations:
        print("Architecture check failed:", file=sys.stderr)
        for violation in sorted(violations):
            print(f"- {violation}", file=sys.stderr)
        return 1

    print(
        "Architecture check passed: "
        f"{len(SERVICES)} code services, {len(discovered)} singular module owners, "
        f"{edge_count} cross-module dependencies."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
