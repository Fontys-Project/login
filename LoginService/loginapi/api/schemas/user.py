from loginapi.models import User
from loginapi.extensions import ma, db
from .role import RoleSchema
from .permission import PermissionSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    # roles = ma.Pluck(RoleSchema(only=("name",)), many=True)
    roles = ma.Pluck('RoleSchema', 'name', many=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
