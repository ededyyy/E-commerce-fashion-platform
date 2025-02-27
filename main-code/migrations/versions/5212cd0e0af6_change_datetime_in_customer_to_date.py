"""change datetime in customer to date

Revision ID: 5212cd0e0af6
Revises: c17e580d12f6
Create Date: 2024-12-24 19:40:46.475403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5212cd0e0af6'
down_revision = 'c17e580d12f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('register_date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('register_date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=False)

    # ### end Alembic commands ###
