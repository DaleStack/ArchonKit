import click
from .helpers import create_app, create_feature

@click.group()
def archonkit():
    """ArchonKit CLI: FastAPI/Django-style scaffolding."""
    pass

@archonkit.command()
@click.argument("app_name")
def new(app_name):
    """Create a new top-level app/project."""
    create_app(app_name)
    click.echo(f"Created new app: {app_name}")

@archonkit.command()
@click.argument("feature_name")
def feature(feature_name):
    """Add a modular app (users, blog, etc.) with clean layout."""
    create_feature(feature_name)
    click.echo(f"Added feature structure for: {feature_name}")

if __name__ == "__main__":
    archonkit()
