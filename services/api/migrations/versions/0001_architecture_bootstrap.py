"""Create the empty non-business architecture baseline.

Revision ID: 0001_architecture_bootstrap
Revises:
Create Date: 2026-07-14
"""

from collections.abc import Sequence

revision: str = "0001_architecture_bootstrap"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Keep the initial baseline intentionally free of business tables."""


def downgrade() -> None:
    """The empty baseline has no database objects to remove."""
