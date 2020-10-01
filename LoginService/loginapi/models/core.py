from loginapi.extensions import db
from sqlalchemy import UniqueConstraint

role_user = company_admin = db.Table(
    'role_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    UniqueConstraint('user_id', 'role_id')
)


class Role(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return "<Role %s>" % self.name


class Permission(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def __repr__(self):
        return "<Permission %s>" % self.name
