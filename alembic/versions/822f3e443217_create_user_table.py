"""Create user table

Revision ID: 822f3e443217
Revises: 6e2a5561f53f
Create Date: 2025-05-14 13:49:58.514681

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '822f3e443217'
down_revision: Union[str, None] = '6e2a5561f53f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
