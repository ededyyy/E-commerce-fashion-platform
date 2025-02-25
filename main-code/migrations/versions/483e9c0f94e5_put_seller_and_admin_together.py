"""put seller and admin together

Revision ID: 483e9c0f94e5
Revises: 3c102bc9cf0f
Create Date: 2024-12-23 11:57:13.273951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483e9c0f94e5'
down_revision = '3c102bc9cf0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_table('admins')
    with op.batch_alter_table('sellers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.drop_constraint('uq_sellers_brandname', type_='unique')
        batch_op.create_unique_constraint('uq_sellers_username', ['username'])
        batch_op.drop_column('lastname')
        batch_op.drop_column('brandname')
        batch_op.drop_column('email')
        batch_op.drop_column('register_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sellers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('register_date', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), nullable=False))
        batch_op.add_column(sa.Column('brandname', sa.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('lastname', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint('uq_sellers_username', type_='unique')
        batch_op.create_unique_constraint('uq_sellers_brandname', ['brandname'])
        batch_op.drop_column('username')

    op.create_table('admins',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), nullable=False),
    sa.Column('password', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
