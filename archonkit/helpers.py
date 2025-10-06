import os

def create_app(app_name):
    os.makedirs(f"{app_name}/core", exist_ok=True)
    os.makedirs(f"{app_name}/templates", exist_ok=True)

    # Create templates/index.html
    with open(f"{app_name}/templates/index.html", "w") as f:
        f.write("<h1>{{ msg }}</h1>")
    
    # Create main.py (as before)
    main_py_content = """
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "msg": "Welcome to ArchonKit!"})
    """.strip()
    with open(f"{app_name}/main.py", "w") as f:
        f.write(main_py_content)
    
    # Create core/database.py
    database_py = """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""".lstrip()
    with open(f"{app_name}/core/database.py", "w") as f:
        f.write(database_py)

    # Create core/config.py 
    config_py = '''
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: str = os.getenv("DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
'''.lstrip()
    with open(f"{app_name}/core/config.py", "w") as f:
        f.write(config_py)

    # Create core/utils.py
    utils_py = '''
from passlib.context import CryptContext
import secrets
from datetime import datetime

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password securely using argon2id."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the argon2id hash."""
    return pwd_context.verify(plain_password, hashed_password)

# --- CSRF Helpers ---

def generate_csrf_token() -> str:
    """Generate a secure CSRF token for forms."""
    return secrets.token_urlsafe(32)

def set_csrf_token_in_session(request) -> str:
    """Generate/set CSRF token in session and return it."""
    token = generate_csrf_token()
    request.session["csrf_token"] = token
    return token

def validate_csrf_token(request, submitted_token: str) -> bool:
    """Check submitted CSRF token against session value."""
    return request.session.get("csrf_token") == submitted_token

# --- Session Regeneration Helper ---

def regenerate_session(request, user_id=None, extra=None):
    """
    Clears the session, sets new authenticated info (prevents fixation).
    """
    request.session.clear()
    if user_id is not None:
        request.session["user_id"] = user_id
        request.session["auth_time"] = datetime.now(timezone.utc).isoformat()
    if extra:
        for k, v in extra.items():
            request.session[k] = v

'''.lstrip()
    with open(f"{app_name}/core/utils.py", "w") as f:
        f.write(utils_py)





def create_feature(feature_name):
    # Create feature directory structure
    os.makedirs(feature_name, exist_ok=True)
    os.makedirs(os.path.join(feature_name, "templates", feature_name), exist_ok=True)
    os.makedirs(os.path.join(feature_name, "static"), exist_ok=True)

    # Create empty forms.py and models.py
    forms_imports = """from pydantic import BaseModel, Field, EmailStr, field_validator
"""
    with open(os.path.join(feature_name, "forms.py"), "w") as f:
        f.write(forms_imports)

    # Write SQLAlchemy + Base imports to models.py
    models_imports = """from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from core.database import Base
"""
    with open(os.path.join(feature_name, "models.py"), "w") as f:
        f.write(models_imports)

    # Boilerplate routes.py with template rendering
    routes_boilerplate = f"""from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="{feature_name}/templates/{feature_name}")

router = APIRouter(
    prefix="/{feature_name}",
    tags=["{feature_name}"]
)

@router.get("/", response_class=HTMLResponse)
async def feature_root(request: Request):
    return templates.TemplateResponse("index.html", {{"request": request, "msg": "Welcome to {feature_name}!"}})
"""
    with open(os.path.join(feature_name, "routes.py"), "w") as f:
        f.write(routes_boilerplate)

    # Boilerplate base.html for template inheritance
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Feature{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""
    with open(os.path.join(feature_name, "templates", feature_name, "base.html"), "w") as f:
        f.write(base_html)

    # Boilerplate index.html extending base.html
    index_html = """{% extends "base.html" %}
{% block content %}
<h1>{{ msg }}</h1>
{% endblock %}
"""
    with open(os.path.join(feature_name, "templates", feature_name, "index.html"), "w") as f:
        f.write(index_html)




def inject_feature_to_main(app_dir, feature_name):
    main_py = os.path.join(app_dir, "main.py")

    import_line = f"import {feature_name}.routes as {feature_name}_routes\n"
    static_line = (
        f"app.mount('/static/{feature_name}', StaticFiles(directory='{feature_name}/static'), name='{feature_name}_static')\n"
    )
    router_line = f"app.include_router({feature_name}_routes.router)\n"

    with open(main_py, "r") as f:
        lines = f.readlines()

    # Insert import_line after the last import
    last_import = max(i for i, l in enumerate(lines) if l.strip().startswith(("import ", "from ")))
    if import_line not in lines:
        lines.insert(last_import + 1, import_line)

    # Insert static_line after the last app.mount (or after app = FastAPI())
    mount_indices = [i for i, l in enumerate(lines) if l.strip().startswith("app.mount")]
    mount_insert_idx = (mount_indices[-1] + 1 if mount_indices else 
                        next(i for i, l in enumerate(lines) if "app = FastAPI()" in l) + 1)
    if static_line not in lines:
        lines.insert(mount_insert_idx, static_line)

    # Insert router_line after the last app.include_router (or after last mount)
    router_indices = [i for i, l in enumerate(lines) if l.strip().startswith("app.include_router")]
    router_insert_idx = (router_indices[-1] + 1 if router_indices else mount_insert_idx + 1)
    if router_line not in lines:
        lines.insert(router_insert_idx, router_line)

    # Deduplicate blank lines (optional: collapse >2 blank lines)
    code = "".join(lines)
    while "\n\n\n" in code:
        code = code.replace("\n\n\n", "\n\n")
    with open(main_py, "w") as f:
        f.write(code)


