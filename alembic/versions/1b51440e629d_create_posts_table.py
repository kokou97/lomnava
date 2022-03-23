"""create posts table

Revision ID: 1b51440e629d
Revises: 
Create Date: 2022-03-23 12:05:28.359086

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b51440e629d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
