"""""Make year_level non-nullable

Revision ID: 300df5f0c826
Revises: 088f10c1e443
Create Date: 2024-11-03 02:18:53.537203

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision = '300df5f0c826'
down_revision = '088f10c1e443'
branch_labels = None
depends_on = None


def upgrade():
    # ### Step 1: Define the 'student' table to reference in the update ###
    student_table = table(
        'student',
        column('id', Integer),
        column('year_level', Integer)
    )

    # ### Step 2: Update any rows where 'year_level' is NULL ###
    op.execute(
        student_table.update().where(student_table.c.year_level == None).values(year_level=7)
    )

    # ### Step 3: Alter the column to make it non-nullable ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('year_level',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### Step 4: Revert the 'year_level' column to be nullable again ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('year_level',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
""

