"""Add images column to apartments table

Revision ID: add_images_column
Revises: fix_missing_columns
Create Date: 2025-01-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_images_column'
down_revision: Union[str, Sequence[str], None] = 'fix_missing_columns'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add images column to apartments table
    # Using PostgreSQL ARRAY type to store array of image URLs (strings)
    op.add_column('apartments', sa.Column('images', postgresql.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove images column from apartments table
    op.drop_column('apartments', 'images')

