"""Add foreign-key to posts table

Revision ID: 20d81eea7ced
Revises: 89407ed0ca22
Create Date: 2022-03-23 14:44:41.707520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20d81eea7ced'
down_revision = '89407ed0ca22'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
