"""Create notes table

Revision ID: 6e2a5561f53f
Revises: 
Create Date: 2025-05-08 17:50:00.648751

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6e2a5561f53f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('notes', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('head', sa.String(), nullable=False),
                    sa.Column('body', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('notes')
