"""empty message

Revision ID: ada94f6a8082
Revises: 4b699c5bd162
Create Date: 2018-06-19 22:14:45.146666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ada94f6a8082'
down_revision = '4b699c5bd162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('autotest_system_setting', sa.Column('is_default', sa.Boolean(), nullable=True))
    op.add_column('autotest_system_setting', sa.Column('is_used', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('autotest_system_setting', 'is_used')
    op.drop_column('autotest_system_setting', 'is_default')
    # ### end Alembic commands ###
