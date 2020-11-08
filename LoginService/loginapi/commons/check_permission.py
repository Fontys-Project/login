from functools import wraps
from flask import abort
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack


def permission_required(keys: list):
    """Wrap function or method with a permission validation based on the logged in user/current_user

    :param keys: Function key
    :type keys: list[str]
    :return: function
    :rtype: function
    """

    def real_decorator(func):
        @wraps(func)
        def decorated_view(klass, *args, **kwargs):
            # Checks if the current user is authenticated
            current_user = ctx_stack.top.jwt_user
            if not current_user:
                return abort(404)
            # Checks if the permission is valid
            for key in keys:
                if not any(perm.name == key for perm in current_user.permissions):
                    return abort(403)
            args = (klass,) + args
            return func(*args, **kwargs)

        return decorated_view

    return real_decorator
