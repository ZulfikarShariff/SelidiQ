"""Added new fields to Lesson model

Revision ID: 7e3d9fcbc6e8
Revises: 4a02fa7d67e2
Create Date: 2024-11-03 18:31:29.198011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3d9fcbc6e8'
down_revision = '4a02fa7d67e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.add_column(sa.Column('critical_thinking_goal', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('creativity_goal', sa.Text(), nullable=True))
        batch_op.alter_column('complexity_level',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('engagement_activity',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('lesson_type',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    with op.batch_alter_table('student_subject', schema=None) as batch_op:
        batch_op.drop_column('score')

    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('student_subject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))

    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.alter_column('lesson_type',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('engagement_activity',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('complexity_level',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('creativity_goal')
        batch_op.drop_column('critical_thinking_goal')

    # ### end Alembic commands ###
