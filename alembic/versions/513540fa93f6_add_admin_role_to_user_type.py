"""add_admin_role_to_user_type

Revision ID: 513540fa93f6
Revises: 8996cd2f80cb
Create Date: 2025-12-19 16:23:41.190374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '513540fa93f6'
down_revision: Union[str, Sequence[str], None] = '8996cd2f80cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE usertype ADD VALUE 'ADMIN'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
