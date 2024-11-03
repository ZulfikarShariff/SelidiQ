"""Add age and year_level to Student model

Revision ID: 088f10c1e443
Revises: 88a672bb244c
Create Date: 2024-11-03 02:07:54.739436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088f10c1e443'
down_revision = '88a672bb244c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('year_level', sa.Integer(), nullable=True))  # Initially nullable


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('year_level')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
