from loginapi.extensions import db


class Permission(db.Model):
    """Basic permission model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def __repr__(self):
        return "<Permission %s>" % self.name
