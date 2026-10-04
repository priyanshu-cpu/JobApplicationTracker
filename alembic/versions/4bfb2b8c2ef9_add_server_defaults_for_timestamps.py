"""add server defaults for timestamps

Revision ID: 4bfb2b8c2ef9
Revises: 1de9bc713ca1
Create Date: 2026-10-04 09:51:39.092366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bfb2b8c2ef9'
down_revision: Union[str, Sequence[str], None] = '1de9bc713ca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("applications", "created_at", server_default=sa.func.now())
    op.alter_column("applications", "updated_at", server_default=sa.func.now())


def downgrade() -> None:
    op.alter_column("applications", "updated_at", server_default=None)
    op.alter_column("applications", "created_at", server_default=None)