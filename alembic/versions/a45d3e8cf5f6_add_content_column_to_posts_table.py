"""add content column to posts table

Revision ID: a45d3e8cf5f6
Revises: 1b51440e629d
Create Date: 2022-03-23 14:15:58.468633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a45d3e8cf5f6'
down_revision = '1b51440e629d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
