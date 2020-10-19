"""add test users

Revision ID: 91032338e81e
Revises: 28db89648641
Create Date: 2020-10-12 19:40:39.433138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91032338e81e'
down_revision = '28db89648641'
branch_labels = None
depends_on = None


def upgrade():
    from loginapi.models.user import User
    user_table = sa.sql.table(
        'user',
        sa.sql.column("username", sa.String),
        sa.sql.column("password", sa.String),
        sa.sql.column("active", sa.Boolean)
    )

    to_insert = [
        {"username": "hans@wmstest.nl", "password": User(password="WachtwoordHans1").password, "active": True},
        {"username": "freek@wmstest.nl", "password": User(password="WachtwoordFreek2").password, "active": True}
    ]
    op.bulk_insert(user_table, to_insert)


def downgrade():
    pass
