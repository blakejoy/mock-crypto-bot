"""empty message

Revision ID: baf945b47294
Revises: 
Create Date: 2017-11-09 17:14:51.504149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baf945b47294'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('account_number', sa.Integer(), nullable=False),
    sa.Column('usd_balance', sa.Float(precision=2), nullable=True),
    sa.Column('btc_balance', sa.Float(precision=2), nullable=True),
    sa.Column('eth_balance', sa.Float(precision=2), nullable=True),
    sa.Column('ltc_balance', sa.Float(precision=2), nullable=True),
    sa.Column('date_opened', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('account_number')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('transaction_type', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('tx_currency', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['transaction_type'], ['transaction_type.id'], ),
    sa.ForeignKeyConstraint(['tx_currency'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.account_number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=192), nullable=False),
    sa.Column('role', sa.SmallInteger(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('first_login', sa.SmallInteger(), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.account_number'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('transactions')
    op.drop_table('wallet')
    op.drop_table('transaction_type')
    op.drop_table('currency')
    # ### end Alembic commands ###
