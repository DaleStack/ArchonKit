import os
import click

def is_valid_name(name):
    """Check if name is valid for Python projects/modules"""
    import re
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name) is not None

@click.group()
@click.version_option()
def cli():
    """ArchonKit: The Fast, Familiar, Full-Stack Python Toolkit."""
    pass


@cli.command()
@click.argument("project_name")
def new(project_name):
    """Create a new ArchonKit project"""

    if not is_valid_name(project_name):
        click.echo("Project name must start with a letter and contain only letters, numbers, and underscores")
        return
    
    if os.path.exists(project_name):
        click.echo(f"Project {project_name} already exists!")
        return

    # Core project structure
    os.makedirs(f"{project_name}/core", exist_ok=True)

    # main.py
    with open(f"{project_name}/main.py", "w") as f:
        f.write(
            '''from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import you app first: from <app_name> import routers as <app_name>.router

app = FastAPI()
# No default app here, use `archonkit add <app_name>` to scaffold apps

# Register Route like this:
# app.include_router(<app_name>.router, prefix="/<app_name>")


# Register Static File:
# app.mount("/static/<app_name>", StaticFiles(directory="<app_name>/static/<app_name>"), name="<app_name>_static")





@app.get("/")
def home():
    return {"message": "Welcome to ArchonKit!"}
'''
        )

    # core/config.py
    with open(f"{project_name}/core/config.py", "w") as f:
        f.write(
            f'''import os

class Settings:
    PROJECT_NAME: str = "{project_name}"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

settings = Settings()
'''
        )

    # core/database.py
    with open(f"{project_name}/core/database.py", "w") as f:
        f.write(
            '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        )

    # core/dependencies.py
    with open(f"{project_name}/core/dependencies.py", "w") as f:
        f.write("# Place shared dependencies here (e.g., auth, common services)\n")

    # core/utils.py
    with open(f"{project_name}/core/utils.py", "w") as f:
        f.write('''# Place helper functions here\n
    from fastapi import Request
    from pydantic import BaseModel
                
    # Form Parsing
    async def parse_form(request: Request, schema: type[BaseModel]) -> BaseModel:
        form_data = await request.form()
        clean_data = {k: v for k, v in form_data.items()}
        return schema(**clean_data)

                
''')

    click.echo(f"Created new ArchonKit project: {project_name}")


@cli.command()
@click.argument("app_name")
def add(app_name):
    """Add a new app to the project"""

    if not is_valid_name(app_name):
        click.echo("App name must start with a letter and contain only letters, numbers, and underscores")
        return
    
    base_path = os.getcwd()
    app_path = os.path.join(base_path, app_name)

    if os.path.exists(app_path):
        click.echo(f"App {app_name} already exists!")
        return

    os.makedirs(f"{app_path}/templates/{app_name}", exist_ok=True)
    os.makedirs(f"{app_path}/static/{app_name}", exist_ok=True)

    with open(f"{app_path}/schema.py", "w") as f:
        f.write("")

    with open(f"{app_path}/__init__.py", "w") as f:
        f.write("")

    with open(f"{app_path}/models.py", "w") as f:
        f.write("# Define your models here\n")

    with open(f"{app_path}/routers.py", "w") as f:
        f.write(
            f'''from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="{app_name}/templates/{app_name}")


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def {app_name}_index(request: Request):
    return templates.TemplateResponse("{app_name}/index.html", {{"request": request}})
'''
        )

    with open(f"{app_path}/templates/{app_name}/index.html", "w") as f:
        f.write(f"<h1>{app_name.title()} App Works!</h1>")

    click.echo(f"Added new app: {app_name}")
