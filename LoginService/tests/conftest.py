import json
import pytest
from dotenv import load_dotenv

from loginapi.models import User, Role, Permission
from loginapi.app import create_app
from loginapi.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory, RoleFactory, PermissionFactory

register(UserFactory)
register(RoleFactory)
register(PermissionFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def create_roles(db, user):
    role_name = "Admin"
    role = Role(name=role_name, users=[user])
    db.session.add(role)
    db.session.commit()

    role_permissions = ["LOGIN_USER_CREATE", "LOGIN_USER_DELETE", "LOGIN_USER_GET", "LOGIN_USER_GET_ALL",
                        "LOGIN_USER_UPDATE"]
    for permission in role_permissions:
        _permission = Permission(name=permission, roles=[role])
        db.session.add(_permission)
        db.session.commit()


@pytest.fixture
def admin_user(db, create_roles):
    user = User(
        username='admin',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
