from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModuleBoundary:
    """Machine-readable declaration of a module's public architecture boundary."""

    name: str
    public_contracts: tuple[str, ...] = ()
    owns_data: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
