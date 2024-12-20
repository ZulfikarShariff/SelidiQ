"""Add first, middle, and last name fields to Student model

Revision ID: f3750c4b2ef3
Revises: None
Create Date: 2024-10-28 22:35:30.306512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3750c4b2ef3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        # Add first_name with a default value to avoid IntegrityError for existing rows
        batch_op.add_column(sa.Column('first_name', sa.String(length=100), nullable=False, server_default='Unknown'))
        # Add middle_name as an optional field
        batch_op.add_column(sa.Column('middle_name', sa.String(length=100), nullable=True))
        # Add last_name with a default value to avoid IntegrityError for existing rows
        batch_op.add_column(sa.Column('last_name', sa.String(length=100), nullable=False, server_default='Unknown'))
        # Remove the old 'name' column
        batch_op.drop_column('name')


def downgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        # Revert the changes made during the upgrade
        batch_op.add_column(sa.Column('name', sa.String(length=255), nullable=False))
        batch_op.drop_column('last_name')
        batch_op.drop_column('middle_name')
        batch_op.drop_column('first_name')

