"""add order number

Revision ID: 84fcd53df198
Revises: d3313af39a6e
Create Date: 2024-12-27 21:37:02.392587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84fcd53df198'
down_revision = 'd3313af39a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_number', sa.String(length=50), nullable=False))
        batch_op.create_unique_constraint('uq_order_number', ['order_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('order_number')

    # ### end Alembic commands ###
