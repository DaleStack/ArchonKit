import click
import os

@click.group()
def archonkit():
    """ArchonKit CLI: FastAPI/Django-style scaffolding."""
    pass

@archonkit.command()
@click.argument("app_name")
def new(app_name):
    """Create a new top-level app/project."""
    os.makedirs(f"{app_name}/core", exist_ok=True)
    with open(f"{app_name}/main.py", "w") as f:
        f.write("# FastAPI entrypoint\n")
    click.echo(f"Created new app: {app_name}")

@archonkit.command()
@click.argument("feature_name")
def feature(feature_name):
    """Add a Django-style feature/app ('users', 'blog', etc)."""
    structure = ["routes", "models", "forms", "templates", "static"]
    for folder in structure:
        path = f"{feature_name}/{folder}"
        os.makedirs(path, exist_ok=True)
        if folder not in ["templates", "static"]:
            open(f"{path}/__init__.py", "a").close()
    click.echo(f"Added feature: {feature_name}")

if __name__ == "__main__":
    archonkit()
