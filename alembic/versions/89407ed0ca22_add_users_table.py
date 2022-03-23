"""Add Users table

Revision ID: 89407ed0ca22
Revises: a45d3e8cf5f6
Create Date: 2022-03-23 14:30:44.715825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89407ed0ca22'
down_revision = 'a45d3e8cf5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass