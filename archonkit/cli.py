import os
import click

@click.group()
@click.version_option()
def cli():
    """ArchonKit: The Fast, Familiar, Full-Stack Python Toolkit."""
    pass

@cli.command()
@click.argument("project_name")
def new(project_name):
    """Create a new ArchonKit project"""
    if os.path.exists(project_name):
        click.echo(f"Project {project_name} already exists!")
        return

    # Base structure
    os.makedirs(f"{project_name}/core", exist_ok=True)
    os.makedirs(f"{project_name}/templates", exist_ok=True)
    os.makedirs(f"{project_name}/static", exist_ok=True)

    # main.py
    with open(f"{project_name}/main.py", "w") as f:
        f.write(
            '''from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Welcome to ArchonKit!"}
'''
        )

    # core/config.py
    with open(f"{project_name}/core/config.py", "w") as f:
        f.write(
            '''import os

class Settings:
    PROJECT_NAME: str = "ArchonKit Project"
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
        f.write("# Place helper functions here\n")

    click.echo(f"Created new ArchonKit project: {project_name}")
