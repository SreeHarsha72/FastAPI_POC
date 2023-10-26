"""add few more columns to posts table

Revision ID: e2af3380fd49
Revises: a0ddf187677d
Create Date: 2023-10-26 09:20:43.986298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2af3380fd49'
down_revision: Union[str, None] = 'a0ddf187677d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts',
                  sa.Column('createdAt', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('Now()')), )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'createdAt')
    pass
