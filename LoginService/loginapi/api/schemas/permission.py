from loginapi.models.core import Permission
from loginapi.extensions import ma, db


class PermissionSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.Int(dump_only=True)

    class Meta:
        model = Permission
        sqla_session = db.session
        load_instance = True
