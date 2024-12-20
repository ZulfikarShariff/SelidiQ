"""Added title field to Lesson model

Revision ID: c2c0c8b769ac
Revises: 83d2db4da74b
Create Date: 2024-10-30 20:02:49.894300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2c0c8b769ac'
down_revision = '83d2db4da74b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        # Adding the 'title' column with a default value to handle existing rows
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=False, server_default="Untitled Lesson"))

    # ### end Alembic commands ###

    # Remove the server default if it’s no longer needed for new rows
    op.alter_column('lesson', 'title', server_default=None)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
