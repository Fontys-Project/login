from loginapi.extensions import db
from sqlalchemy import UniqueConstraint

role_user = db.Table(
    'role_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    UniqueConstraint('user_id', 'role_id')
)

role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    UniqueConstraint('role_id', 'permission_id')
)


class Role(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    users = db.relationship(
        'User',
        secondary=role_user,
        backref=db.backref('roles', lazy='joined')
    )
    permissions = db.relationship(
        'Permission',
        secondary=role_permission,
        backref=db.backref('roles', lazy='joined')
    )

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return "<Role %s>" % self.name


class Permission(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def __repr__(self):
        return "<Permission %s>" % self.name

    def __eq__(self, other):
        return self.name == other.name
