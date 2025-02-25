"""add refund and return enum to order status

Revision ID: eb0f5c73884b
Revises: c90b647f20e6
Create Date: 2024-12-26 18:56:50.694607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0f5c73884b'
down_revision = 'c90b647f20e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.Enum('Pending Payment', 'Pending Shipment', 'In Transit', 'Completed', 'Refund and Return', name='order_status'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('Pending Payment', 'Pending Shipment', 'In Transit', 'Completed', 'Refund and Return', name='order_status'),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)

    # ### end Alembic commands ###
