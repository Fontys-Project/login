from loginapi.models import User
from loginapi.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    roles = ma.Pluck('RoleSchema', 'name', many=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
