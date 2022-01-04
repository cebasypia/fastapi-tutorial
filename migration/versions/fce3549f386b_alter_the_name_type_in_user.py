"""Alter the name type in user

Revision ID: fce3549f386b
Revises: db4c7c8a96b3
Create Date: 2022-01-01 20:05:36.160818

"""
# import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql.sqltypes import String

# revision identifiers, used by Alembic.
revision = "fce3549f386b"
down_revision = "db4c7c8a96b3"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("user", "name", type_=String(50))


def downgrade():
    op.alter_column("user", "name", type_=String(10))
