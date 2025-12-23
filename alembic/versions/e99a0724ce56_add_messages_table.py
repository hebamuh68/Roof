"""add_messages_table

Revision ID: e99a0724ce56
Revises: f4973d60beb4
Create Date: 2025-12-22 20:38:52.833125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'e99a0724ce56'
down_revision: Union[str, Sequence[str], None] = 'f4973d60beb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('apartment_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['apartment_id'], ['apartments.id'], ondelete='SET NULL'),
    )

    # Create indexes for better query performance
    op.create_index('idx_messages_sender', 'messages', ['sender_id'])
    op.create_index('idx_messages_receiver', 'messages', ['receiver_id'])
    op.create_index('idx_messages_conversation', 'messages', ['sender_id', 'receiver_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])
    op.create_index('idx_messages_apartment', 'messages', ['apartment_id'])
 

def downgrade():
    op.drop_index('idx_messages_apartment', table_name='messages')
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation', table_name='messages')
    op.drop_index('idx_messages_receiver', table_name='messages')
    op.drop_index('idx_messages_sender', table_name='messages')
    op.drop_table('messages')
