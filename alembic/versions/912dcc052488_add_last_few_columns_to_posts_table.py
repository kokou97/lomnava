"""add last few columns to posts table

Revision ID: 912dcc052488
Revises: 20d81eea7ced
Create Date: 2022-03-23 14:50:13.737123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '912dcc052488'
down_revision = '20d81eea7ced'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
