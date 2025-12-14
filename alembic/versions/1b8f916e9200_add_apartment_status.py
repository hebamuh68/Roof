"""add_apartment_status

Revision ID: 1b8f916e9200
Revises: 3ae513282433
Create Date: 2025-12-14 18:00:36.834713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b8f916e9200'
down_revision: Union[str, Sequence[str], None] = '3ae513282433'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create enum type
    op.execute("CREATE TYPE apartment_status AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED')")

    # Add status column with default PUBLISHED for existing records
    op.add_column('apartments',
        sa.Column('status', sa.Enum('DRAFT', 'PUBLISHED', 'ARCHIVED', name='apartment_status'),
                  nullable=False, server_default='PUBLISHED')
    )

def downgrade():
    op.drop_column('apartments', 'status')
    op.execute("DROP TYPE apartment_status")