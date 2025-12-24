"""add_notifications_table

Revision ID: d760f419c9a2
Revises: e99a0724ce56
Create Date: 2025-12-24 22:38:15.918802
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'd760f419c9a2'
down_revision: Union[str, Sequence[str], None] = 'e99a0724ce56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None





def upgrade() -> None:
    # Create notification type enum (using raw SQL to handle if exists)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE notificationtype AS ENUM ('new_message', 'apartment_inquiry', 'system');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column(
            'user_id',
            sa.Integer(),
            sa.ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False
        ),
        sa.Column(
            'type',
            postgresql.ENUM(
                'new_message',
                'apartment_inquiry',
                'system',
                name='notificationtype',
                create_type=False
            ),
            nullable=False
        ),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('is_read', sa.Boolean(), default=False, nullable=False),
        sa.Column('data', postgresql.JSON(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(),
            default=sa.func.now(),
            nullable=False
        ),
    )

    # Create indexes
    op.create_index(
        'idx_notifications_user_id',
        'notifications',
        ['user_id']
    )
    op.create_index(
        'idx_notifications_user_read',
        'notifications',
        ['user_id', 'is_read']
    )
    op.create_index(
        'idx_notifications_created_at',
        'notifications',
        ['created_at']
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_notifications_created_at', table_name='notifications')
    op.drop_index('idx_notifications_user_read', table_name='notifications')
    op.drop_index('idx_notifications_user_id', table_name='notifications')

    # Drop table
    op.drop_table('notifications')

    # Drop enum type
    op.execute('DROP TYPE notificationtype')