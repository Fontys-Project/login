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

permissions = [
    {"name": "LOGIN_USER_CREATE"},
    {"name": "LOGIN_USER_GET"},
    {"name": "LOGIN_USER_GET_ALL"},
    {"name": "LOGIN_USER_UPDATE"},
    {"name": "LOGIN_USER_DELETE"},
    {"name": "CUSTOMER_CUSTOMER_CREATE_OTHER"},
    {"name": "CUSTOMER_CUSTOMER_GET_SELF"},
    {"name": "CUSTOMER_CUSTOMER_GET_OTHER"},
    {"name": "CUSTOMER_CUSTOMER_GET_ALL"},
    {"name": "CUSTOMER_CUSTOMER_UPDATE_SELF"},
    {"name": "CUSTOMER_CUSTOMER_UPDATE_OTHER"},
    {"name": "CUSTOMER_CUSTOMER_DELETE_SELF"},
    {"name": "CUSTOMER_CUSTOMER_DELETE_OTHER"},
    {"name": "inventory_product_getall"},
    {"name": "inventory_product_get"},
    {"name": "inventory_product_modify"},
    {"name": "inventory_product_add"},
    {"name": "inventory_product_delete"},
    {"name": "inventory_tag_getall"},
    {"name": "inventory_tag_get"},
    {"name": "inventory_tag_modify"},
    {"name": "inventory_tag_add"},
    {"name": "inventory_tag_delete"},
    {"name": "inventory_tag_applytag"},
    {"name": "inventory_stock_getall"},
    {"name": "inventory_stock_get"},
    {"name": "inventory_stock_modify"},
    {"name": "inventory_stock_add"},
    {"name": "inventory_stock_delete"},
]
roles = [
    {"name": "Admin"},
    {"name": "Gebruiker"},
]


def lookup_role_id(name):
    conn = op.get_bind()
    res = conn.execute("SELECT id FROM role WHERE name like '%s'" % name)
    res = res.fetchone()
    if res is not None:
        return res['id']
    return None


def lookup_permission_id(name):
    conn = op.get_bind()
    res = conn.execute("SELECT id FROM permission WHERE name like '%s'" % name)
    res = res.fetchone()
    if res is not None:
        return res['id']
    return None


def lookup_role_permission_id(rid, pid):
    conn = op.get_bind()
    res = conn.execute(
        "SELECT role_id, permission_id FROM role_permission WHERE role_id = %s AND permission_id = %s" % (rid, pid))
    res = res.fetchone()
    if res is not None:
        return res
    return None


def lookup_user_id(username):
    conn = op.get_bind()
    res = conn.execute(
        "SELECT id FROM user WHERE username like '%s'" % username)
    res = res.fetchone()
    if res is not None:
        return res['id']
    return None


def prepare_insert_permissions():
    permission_insert_data = []
    for entry in permissions:
        pid = lookup_permission_id(entry['name'])
        if pid is None:
            permission_insert_data.append(entry)
    return permission_insert_data


def prepare_insert_roles():
    role_insert_data = []
    for entry in roles:
        rid = lookup_role_id(entry['name'])
        if rid is None:
            role_insert_data.append(entry)
    return role_insert_data


def prepare_role_permission():
    rid = lookup_role_id("Admin")
    role_permission_insert_data = []
    for entry in permissions:
        pid = lookup_permission_id(entry['name'])
        rpid = lookup_role_permission_id(rid, pid)
        if rpid is None:
            role_permission_insert_data.append({
                "role_id": rid,
                "permission_id": pid
            })
    return role_permission_insert_data


def upgrade():
    # define tables
    role_table = sa.sql.table(
        'role',
        sa.sql.column("name", sa.String),
    )
    permission_table = sa.sql.table(
        'permission',
        sa.sql.column("name", sa.String),
    )
    role_permission_table = sa.sql.table(
        'role_permission',
        sa.sql.column("role_id", sa.Integer),
        sa.sql.column("permission_id", sa.Integer),
    )
    user_role_table = sa.sql.table(
        'role_user',
        sa.sql.column("user_id", sa.Integer),
        sa.sql.column("role_id", sa.Integer)
    )

    # insert permissions
    _permissions = prepare_insert_permissions()
    op.bulk_insert(permission_table, _permissions)

    # insert roles
    _roles = prepare_insert_roles()
    op.bulk_insert(role_table, _roles)

    # insert role_permission, admin user only
    _role_permissions = prepare_role_permission()
    if len(_role_permissions) > 0:
        op.bulk_insert(
            role_permission_table,
            _role_permissions
        )

    # link admin role to user
    uid = lookup_user_id("admin@wmstest.nl")
    rid = lookup_role_id("Admin")
    op.bulk_insert(user_role_table, [{
        "user_id": uid,
        "role_id": rid
    }])


def downgrade():
    pass
