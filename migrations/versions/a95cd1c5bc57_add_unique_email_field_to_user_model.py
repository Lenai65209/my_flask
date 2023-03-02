"""add unique email field to user model

Revision ID: a95cd1c5bc57
Revises: 
Create Date: 2023-02-28 23:13:56.641202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a95cd1c5bc57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=255), server_default='', nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('_password', sa.LargeBinary(), nullable=True),
    sa.Column('first_name', sa.String(length=120), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=120), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###