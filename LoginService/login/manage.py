import click
from flask.cli import FlaskGroup

from login.app import create_app


def create_login(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_login)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from login.extensions import db
    from login.models import User

    click.echo("create user")
    user = User(username="admin", email="m.devrees@gmail.com", password="Password123", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
