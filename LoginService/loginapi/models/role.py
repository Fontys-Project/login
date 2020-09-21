from loginapi.extensions import db


class Role(db.Model):
    """Basic role model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship("Permission", backref="roles")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return "<Role %s>" % self.name
