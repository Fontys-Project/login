from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from loginapi.api.schemas import RoleSchema
from loginapi.models import Role
from loginapi.extensions import db
from loginapi.commons.pagination import paginate


class RoleResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
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
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required]

    def get(self, role_id):
        schema = RoleSchema()
        _role = Role.query.get_or_404(role_id)
        return {"role": schema.dump(_role)}

    def put(self, role_id):
        schema = RoleSchema(partial=True)
        _role = Role.query.get_or_404(role_id)
        role = schema.load(request.json, instance=_role)

        db.session.commit()

        return {"msg": "role updated", "role": schema.dump(role)}

    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()

        return {"msg": "role deleted"}


class RoleList(Resource):
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
        schema = RoleSchema(many=True)
        query = Role.query
        return paginate(query, schema)

    def post(self):
        schema = RoleSchema()

        role = schema.load(request.json)

        db.session.add(role)
        db.session.commit()

        return {"msg": "role created", "role": schema.dump(role)}, 201
