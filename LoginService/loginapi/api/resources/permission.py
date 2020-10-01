from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from loginapi.api.schemas import PermissionSchema
from loginapi.models import Permission
from loginapi.extensions import db
from loginapi.commons.pagination import paginate


class PermissionResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: permission_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  permission: PermissionSchema
        404:
          description: permission does not exist
    put:
      tags:
        - api
      parameters:
        - in: path
          name: permission_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              PermissionSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: permission updated
                  user: PermissionSchema
        404:
          description: permission does not exist
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: permission_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: permission deleted
        404:
          description: permission does not exists
    """

    # method_decorators = [jwt_required]

    def get(self, permission_id):
        schema = PermissionSchema()
        permission = Permission.query.get_or_404(permission_id)
        return {"user": schema.dump(permission)}

    @jwt_required
    def put(self, permission_id):
        schema = PermissionSchema(partial=True)
        permission = Permission.query.get_or_404(permission_id)
        permission = schema.load(request.json, instance=permission)

        db.session.commit()

        return {"msg": "permission updated", "permission": schema.dump(permission)}

    @jwt_required
    def delete(self, permission_id):
        permission = Permission.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()

        return {"msg": "permission deleted"}


class PermissionList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = PermissionSchema(many=True)
        query = Permission.query
        return paginate(query, schema)

    def post(self):
        schema = PermissionSchema()
        permission = schema.load(request.json)

        db.session.add(permission)
        db.session.commit()

        return {"msg": "permission created", "permission": schema.dump(permission)}, 201
