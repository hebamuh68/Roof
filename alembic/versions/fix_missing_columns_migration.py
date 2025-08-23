"""Fix missing columns and update schema

Revision ID: fix_missing_columns
Revises: aa1680057b85
Create Date: 2025-01-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fix_missing_columns'
down_revision: Union[str, Sequence[str], None] = 'aa1680057b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the UserType enum
    usertype_enum = sa.Enum('seeker', 'renter', name='usertype')
    usertype_enum.create(op.get_bind())
    
    # Add missing columns to users table
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False, server_default=''))
    op.add_column('users', sa.Column('role', usertype_enum, nullable=False, server_default='seeker'))
    
    # Add missing foreign key to apartments table
    op.add_column('apartments', sa.Column('renter_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_apartments_renter_id_users', 'apartments', 'users', ['renter_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign key from apartments table
    op.drop_constraint('fk_apartments_renter_id_users', 'apartments', type_='foreignkey')
    op.drop_column('apartments', 'renter_id')
    
    # Remove columns from users table
    op.drop_column('users', 'role')
    op.drop_column('users', 'hashed_password')
    
    # Drop the UserType enum
    sa.Enum(name='usertype').drop(op.get_bind()) 