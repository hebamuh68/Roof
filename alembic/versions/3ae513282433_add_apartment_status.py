"""add_apartment_status

Revision ID: 3ae513282433
Revises: add_images_column
Create Date: 2025-12-14 17:59:55.148304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ae513282433'
down_revision: Union[str, Sequence[str], None] = 'add_images_column'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
