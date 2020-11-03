"""Add default roles and LOGIN permissions to db

Revision ID: eb10bd857c49
Revises: 91032338e81e
Create Date: 2020-11-03 18:18:25.866110

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eb10bd857c49'
down_revision = '91032338e81e'
branch_labels = None
depends_on = None


def upgrade():
    from loginapi.models import Permission, Role, User
    role_table = sa.sql.table(
        'role',
        sa.sql.column("name", sa.String),
    )
    permission_table = sa.sql.table(
        'permission',
        sa.sql.column("name", sa.String),
    )

    permissions = [
        {"name": "LOGIN_USER_CREATE"},
        {"name": "LOGIN_USER_READ"},
        {"name": "LOGIN_USER_READ_ALL"},
        {"name": "LOGIN_USER_UPDATE"},
        {"name": "LOGIN_USER_DELETE"},
    ]
    roles = [
        {"name": "Admin"},
        {"name": "Gebruiker"},
    ]
    op.bulk_insert(permission_table, permissions)
    op.bulk_insert(role_table, roles)


def downgrade():
    pass
