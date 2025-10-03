import click
from .helpers import create_app, create_feature, inject_feature_to_main

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
@click.argument("app_dir", default=".")
def feature(feature_name, app_dir):
    """Add a modular app (users, blog, etc.) and inject into main.py."""
    create_feature(feature_name)
    inject_feature_to_main(app_dir, feature_name)
    click.echo(f"Added feature structure for: {feature_name} and wired it into {app_dir}/main.py")

if __name__ == "__main__":
    archonkit()
