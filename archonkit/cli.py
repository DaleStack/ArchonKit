import click
from .helpers import create_app, create_feature, inject_feature_to_main
import secrets
import typer
from alembic.config import Config
from alembic import command as alembic_cmd

app = typer.Typer()

@click.group()
def archonkit():
    """ArchonKit CLI: FastAPI/Django-style scaffolding."""
    pass

# Scaffold App
@archonkit.command()
@click.argument("app_name")
def new(app_name):
    """Create a new top-level app/project."""
    create_app(app_name)
    click.echo(f"Created new app: {app_name}")

# Scaffold Feature
@archonkit.command()
@click.argument("feature_name")
@click.argument("app_dir", default=".")
def feature(feature_name, app_dir):
    """Add a modular app (users, blog, etc.) and inject into main.py."""
    create_feature(feature_name)
    inject_feature_to_main(app_dir, feature_name)
    click.echo(f"Added feature structure for: {feature_name} and wired it into {app_dir}/main.py")

# Generate Key for SECRET_KEY
@archonkit.command()
@click.option('--length', default=64, help='Length of the secret key (default: 64 bytes, prints 128 hex characters).')
def keygen(length):
    """Generate a cryptographically secure secret key."""
    key = secrets.token_hex(length)
    click.echo(f"Your secret key:\n{key}")

# ALEMBIC COMMANDS
def get_alembic_config():
    return Config("alembic.ini")

@archonkit.command()
@click.argument("message")
def makemigrations(message):
    """Create a new Alembic migration with autogeneration and a message."""
    cfg = get_alembic_config()
    alembic_cmd.revision(cfg, message=message, autogenerate=True)
    click.echo(f"Migration created: {message}")

@archonkit.command()
def migrate():
    """Apply all Alembic migrations (upgrade head)."""
    cfg = get_alembic_config()
    alembic_cmd.upgrade(cfg, "head")
    click.echo("Database upgraded to head.")

@archonkit.command()
@click.argument("revision", default="-1")
def rollback(revision):
    """
    Downgrade (rollback) the database schema.
    By default, rolls back one migration step.
    Example: archonkit rollback         # rollback one step
             archonkit rollback base    # rollback to base
             archonkit rollback <rev>   # rollback to a specific revision
    """
    cfg = get_alembic_config()
    alembic_cmd.downgrade(cfg, revision)
    click.echo(f"Database rolled back to revision: {revision}")


if __name__ == "__main__":
    archonkit()
