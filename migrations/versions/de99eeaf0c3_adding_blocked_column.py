"""adding blocked column

Revision ID: de99eeaf0c3
Revises: 168b3152daff
Create Date: 2014-09-19 11:02:48.054298

"""

# revision identifiers, used by Alembic.
revision = 'de99eeaf0c3'
down_revision = '168b3152daff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('blocked', sa.BOOLEAN,
                                     default=False, server_default="false", nullable=False))


def downgrade():
    op.drop_column('users', 'blocked')
