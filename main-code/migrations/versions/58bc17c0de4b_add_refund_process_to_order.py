"""add refund process to order

Revision ID: 58bc17c0de4b
Revises: 535725891e72
Create Date: 2024-12-28 21:58:20.752603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58bc17c0de4b'
down_revision = '535725891e72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refund_processed', sa.Boolean(), nullable=True))
    op.execute('UPDATE orders SET refund_processed = False WHERE refund_processed IS NULL')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('refund_processed', nullable=False)

    # ### end Alembic commands ###



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('refund_processed')

    # ### end Alembic commands ###
