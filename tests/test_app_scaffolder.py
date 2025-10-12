import os
import sys
from pathlib import Path

import pytest

# Ensure package import works
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from archonkit.helpers.app_scaffold import create_app


@pytest.fixture
def tmp_project_dir(tmp_path):
    """Creates isolated directory for tests."""
    cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(cwd)


def test_create_app_creates_structure(tmp_project_dir):
    """Should create all core folders and essential files."""
    app_name = "demoapp"
    create_app(app_name)
    app_dir = tmp_project_dir / app_name

    # --- Directories ---
    assert (app_dir / "core").exists()
    assert (app_dir / "templates").exists()

    # --- Files ---
    assert (app_dir / "main.py").exists()
    assert (app_dir / "templates" / "index.html").exists()

    # --- Core Modules ---
    for fname in [
        "config.py",
        "database.py",
        "utils.py",
        "decorators.py",
        "messages.py",
        "admin_loader.py",
    ]:
        assert (app_dir / "core" / fname).exists()


def test_main_py_contains_fastapi_setup(tmp_project_dir):
    """main.py should define FastAPI app and root route."""
    app_name = "demoapp"
    create_app(app_name)
    main_py = Path(app_name) / "main.py"
    code = main_py.read_text()

    assert "FastAPI" in code
    assert "Request" in code
    assert "HTMLResponse" in code
    assert "Jinja2Templates" in code
    assert "SessionMiddleware" in code
    assert "def root" in code
    assert "TemplateResponse" in code
    assert "Welcome to ArchonKit!" in code


def test_index_html_contains_welcome_message(tmp_project_dir):
    """templates/index.html should contain the correct Jinja syntax."""
    app_name = "demoapp"
    create_app(app_name)
    html = (Path(app_name) / "templates" / "index.html").read_text().strip()

    assert html == "<h1>{{ msg }}</h1>"


def test_config_file_uses_pydantic_settings(tmp_project_dir):
    """core/config.py should define a Settings class using BaseSettings."""
    app_name = "demoapp"
    create_app(app_name)
    config_py = Path(app_name) / "core" / "config.py"
    code = config_py.read_text()

    assert "class Settings" in code
    assert "BaseSettings" in code
    assert "DATABASE_URL" in code
    assert "SECRET_KEY" in code
    assert "DEBUG" in code
    assert "Settings()" in code


def test_database_file_defines_get_db(tmp_project_dir):
    """core/database.py should define get_db generator."""
    app_name = "demoapp"
    create_app(app_name)
    code = (Path(app_name) / "core" / "database.py").read_text()

    assert "create_engine" in code
    assert "SessionLocal" in code
    assert "declarative_base" in code
    assert "def get_db" in code
    assert "yield db" in code


def test_utils_contains_security_helpers(tmp_project_dir):
    """core/utils.py should contain password and CSRF helpers."""
    app_name = "demoapp"
    create_app(app_name)
    code = (Path(app_name) / "core" / "utils.py").read_text()

    for keyword in [
        "hash_password",
        "verify_password",
        "generate_csrf_token",
        "set_csrf_token_in_session",
        "validate_csrf_token",
        "regenerate_session",
    ]:
        assert keyword in code


def test_decorators_defines_login_required(tmp_project_dir):
    """core/decorators.py should define login_required decorator."""
    app_name = "demoapp"
    create_app(app_name)
    code = (Path(app_name) / "core" / "decorators.py").read_text()

    assert "login_required" in code
    assert "RedirectResponse" in code
    assert "SessionLocal" in code
    assert "get_user_model" in code


def test_messages_module_has_add_and_pop_all(tmp_project_dir):
    """core/messages.py should define message queue helpers."""
    app_name = "demoapp"
    create_app(app_name)
    code = (Path(app_name) / "core" / "messages.py").read_text()

    for fn in ["add(", "success(", "info(", "warning(", "error(", "pop_all("]:
        assert fn in code


def test_admin_loader_registers_modelviews(tmp_project_dir):
    """core/admin_loader.py should have register_admin_views logic."""
    app_name = "demoapp"
    create_app(app_name)
    code = (Path(app_name) / "core" / "admin_loader.py").read_text()

    assert "register_admin_views" in code
    assert "ModelView" in code
    assert "importlib" in code
