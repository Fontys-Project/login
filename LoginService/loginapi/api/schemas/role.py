from loginapi.models.core import Role
from loginapi.extensions import ma, db
from .permission import PermissionSchema


class RoleSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    name = ma.String(dump_only=True)
    permissions = ma.Nested(PermissionSchema(only=("name",)), many=True)

    class Meta:
        model = Role
        sqla_session = db.session
        load_instance = True
