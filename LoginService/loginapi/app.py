from flask import Flask

from loginapi import auth, api
from loginapi.extensions import db, jwt, migrate, apispec, celery


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("loginapi")
    app.config.from_object("loginapi.config")

    use_rs256(app)

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def use_rs256(app=None):
    app = app or create_app()
    if app.config['SECRET_KEY'] is None:
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            secret_key = open(dir_path+'/keys/rs256.pem').read()
            public_key = open(dir_path+'/keys/rs256.pub').read()
            app.config.update(
                JWT_ALGORITHM='RS256',
                JWT_PRIVATE_KEY=secret_key,
                JWT_PUBLIC_KEY=public_key
            )
        except Exception as e:
            print("Something went wrong: %s" % str(e))


