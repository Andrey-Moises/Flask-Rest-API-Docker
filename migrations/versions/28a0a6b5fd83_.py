"""empty message

Revision ID: 28a0a6b5fd83
Revises: cf9a5b17915e
Create Date: 2025-01-26 11:48:13.837901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28a0a6b5fd83'
down_revision = 'cf9a5b17915e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
