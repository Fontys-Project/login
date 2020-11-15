from flask import url_for
from loginapi.models import User


def test_get_user(client, db, user, admin_headers, create_roles, mocker):
    # test 404
    # user_url = url_for('api.user_by_id', user_id="100000")

    mocker.patch("loginapi.commons.check_permission.get_current_user", return_value=user)

    user_url = url_for('api.user_self')
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_url = url_for('api.user_by_id', user_id=user.id)
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["active"] == user.active


def test_put_user(client, db, user, admin_headers, mocker):
    mocker.patch("loginapi.commons.check_permission.get_current_user", return_value=user)

    # test 404
    user_url = url_for('api.user_by_id', user_id="100000")
    rep = client.put(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {"username": "updated"}

    user_url = url_for('api.user_by_id', user_id=user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["active"] == user.active


def test_delete_user(client, db, user, admin_headers, mocker):
    mocker.patch("loginapi.commons.check_permission.get_current_user", return_value=user)

    # test 404
    user_url = url_for('api.user_by_id', user_id="100000")
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user

    user_url = url_for('api.user_by_id', user_id=user.id)
    rep = client.delete(user_url,  headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_create_user(client, db, admin_headers):
    # test bad data
    users_url = url_for('api.users')
    data = {"username": "created@mail.com"}
    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["password"] = "admin"

    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created@mail.com"


def test_get_all_user(client, db, user_factory, admin_headers):
    users_url = url_for('api.users')
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(users_url, headers=admin_headers)
    assert rep.status_code == 403

    # results = rep.get_json()
    # for user in users:
    #     assert any(u["id"] == user.id for u in results["results"])
