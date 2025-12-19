"""add_featured_to_apartments

Revision ID: 8996cd2f80cb
Revises: fa1cab7e62f2
Create Date: 2025-12-14 19:06:38.845620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8996cd2f80cb'
down_revision: Union[str, Sequence[str], None] = 'fa1cab7e62f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('apartments',
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false')
    )
    op.add_column('apartments',
        sa.Column('featured_until', sa.DateTime(), nullable=True)
    )
    op.add_column('apartments',
        sa.Column('featured_priority', sa.Integer(), nullable=False, server_default='0')
    )

    # Create index for efficient featured queries
    op.create_index('idx_featured_apartments', 'apartments', ['is_featured', 'featured_priority'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_featured_apartments')
    op.drop_column('apartments', 'is_featured')
    op.drop_column('apartments', 'featured_until')
    op.drop_column('apartments', 'featured_priority')
