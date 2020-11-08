from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from loginapi.api.schemas import UserSchema
from loginapi.models import User, Role
from loginapi.extensions import db
from loginapi.commons.pagination import paginate
from loginapi.commons.check_permission import permission_required
import re

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack


class UserResource(Resource):
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

    def get(self, user_id=False):
        if not user_id:
            return self.get_self()
        return self.get_other(user_id)
        # schema = UserSchema()
        # _user = User.query.get_or_404(user_id)
        # return {"user": schema.dump(_user)}

    @staticmethod
    def get_self():
        schema = UserSchema()
        current_user = ctx_stack.top.jwt_user
        _user = User.query.get_or_404(current_user.id)
        return {"user": schema.dump(_user)}

    @permission_required(["LOGIN_USER_GET"])
    def get_other(self, user_id):
        schema = UserSchema()
        _user = User.query.get_or_404(user_id)
        return {"user": schema.dump(_user)}

    @permission_required(["LOGIN_USER_UPDATE"])
    def put(self, user_id):
        schema = UserSchema(partial=True)
        _user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=_user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    @permission_required(["LOGIN_USER_DELETE"])
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UserList(Resource):
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

    @jwt_required
    @permission_required("LOGIN_USER_GET_ALL")
    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()

        user = schema.load(request.json)
        regex = r'[^@]+@[^@]+\.[^@]+'
        if not re.fullmatch(regex, user.username):
            return {"msg": "Invalid username (add email address)"}, 400

        db.session.add(user)
        db.session.commit()

        role = db.session.query(Role).filter(Role.name == "Gebruiker").first()
        if role:
            user.roles.append(role)
            db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
