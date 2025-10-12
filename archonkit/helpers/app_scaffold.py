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
    config_py = """
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_MODULES = []

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: str = os.getenv("DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
""".lstrip()
    with open(f"{app_name}/core/config.py", "w") as f:
        f.write(config_py)

    # Create core/utils.py
    utils_py = '''
from passlib.context import CryptContext
import secrets
from datetime import datetime, timezone

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

    # Create core/decorators.py
    decorators_py = '''
from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from core.config import settings
from core.database import SessionLocal
import importlib


def get_user_model():
    """Dynamically import the configured AUTH_USER_MODEL (e.g. 'app.models.User')."""
    module_name, class_name = settings.AUTH_USER_MODEL.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def login_required(func):
    """
    Ensures a user is authenticated and attaches `request.state.user`.

    - Automatically detects the FastAPI Request object from args/kwargs.
    - Uses session['user_id'] to fetch the user from the configured AUTH_USER_MODEL.
    - Redirects to settings.LOGIN_URL if unauthenticated or user not found.
    - Attaches both `request.state.user_id` and `request.state.user`.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Find the Request object
        request: Request = kwargs.get("request") or next(
            (arg for arg in args if isinstance(arg, Request)), None
        )
        if not request:
            raise RuntimeError("Request object not found in route handler.")

        # Get user_id from session
        user_id = request.session.get("user_id")
        if not user_id:
            login_url = getattr(settings, "LOGIN_URL", None)
            if login_url:
                return RedirectResponse(url=login_url, status_code=303)
            raise RuntimeError("LOGIN_URL not configured in settings.")

        # Load user model dynamically
        User = get_user_model()

        # Fetch user from DB
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
        finally:
            db.close()

        if not user:
            login_url = getattr(settings, "LOGIN_URL", None)
            if login_url:
                return RedirectResponse(url=login_url, status_code=303)
            raise RuntimeError("LOGIN_URL not configured in settings.")

        # Attach to request.state for downstream access
        request.state.user_id = user_id
        request.state.user = user

        return await func(*args, **kwargs)

    return wrapper

'''.lstrip()
    with open(f"{app_name}/core/decorators.py", "w") as f:
        f.write(decorators_py)

    messages_py = """
from typing import Any, Dict, List, Optional
from fastapi import Request

_STORAGE_KEY = "_messages"

def add(request: Request, message: str, level: str = "info",
        tags: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
    queue: List[Dict[str, Any]] = request.session.get(_STORAGE_KEY, [])
    item: Dict[str, Any] = {"message": message, "level": level}
    if tags:
        item["tags"] = tags
    if data:
        item["data"] = data
    queue.append(item)
    request.session[_STORAGE_KEY] = queue

def success(request: Request, message: str, tags: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
    add(request, message, "success", tags, data)

def info(request: Request, message: str, tags: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
    add(request, message, "info", tags, data)

def warning(request: Request, message: str, tags: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
    add(request, message, "warning", tags, data)

def error(request: Request, message: str, tags: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
    add(request, message, "error", tags, data)

def pop_all(request: Request) -> List[Dict[str, Any]]:
    msgs: List[Dict[str, Any]] = request.session.get(_STORAGE_KEY, [])
    if msgs:
        request.session[_STORAGE_KEY] = []
    return msgs

""".lstrip()
    with open(f"{app_name}/core/messages.py", "w") as f:
        f.write(messages_py)

    admin_loader_py = """
# core/admin_loader.py
import importlib
import pkgutil
from sqladmin import Admin
from sqladmin import ModelView


def register_admin_views(admin: Admin, module_names: list[str]):
    
    # Automatically imports all admin modules and registers all ModelView subclasses.
    # Supports both 'app' and 'app.admin' module names.

    for name in module_names:
        # Try to handle both 'app' and 'app.admin'
        try:
            package = importlib.import_module(name)
        except ModuleNotFoundError:
            # maybe it was just the app name (e.g. 'users')
            try:
                package = importlib.import_module(f"{name}.admin")
            except ModuleNotFoundError:
                continue

        # If the module itself is the admin module, skip iterating
        if not hasattr(package, "__path__"):
            module = package
        else:
            # find its admin.py submodule
            try:
                module = importlib.import_module(f"{name}.admin")
            except ModuleNotFoundError:
                continue

        # Now scan for subclasses of ModelView
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, ModelView)
                and attr is not ModelView
            ):
                admin.add_view(attr)

""".lstrip()
    with open(f"{app_name}/core/admin_loader.py", "w") as f:
        f.write(admin_loader_py)
