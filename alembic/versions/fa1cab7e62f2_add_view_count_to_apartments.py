"""add_view_count_to_apartments

Revision ID: fa1cab7e62f2
Revises: 1b8f916e9200
Create Date: 2025-12-14 19:02:55.026905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa1cab7e62f2'
down_revision: Union[str, Sequence[str], None] = '1b8f916e9200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('apartments',
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0')
    )
    op.add_column('apartments',
        sa.Column('last_viewed_at', sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('apartments', 'view_count')
    op.drop_column('apartments', 'last_viewed_at')
