import os
import sys
from pathlib import Path

import pytest

# Ensure imports work from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from archonkit.helpers.feature_scaffold import create_feature  # noqa: E402
from archonkit.helpers.feature_scaffold import inject_feature_to_main


@pytest.fixture
def tmp_project_dir(tmp_path):
    """Creates isolated directory for tests."""
    cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(cwd)


# ---------------------------------------------------------
#  TESTS FOR create_feature()
# ---------------------------------------------------------


def test_create_feature_creates_directory_structure(tmp_project_dir):
    """Should create feature directories with correct structure."""
    feature_name = "users"
    create_feature(feature_name)

    feature_dir = tmp_project_dir / feature_name
    assert feature_dir.exists()
    assert feature_dir.is_dir()

    # Check nested template directory
    templates_dir = feature_dir / "templates" / feature_name
    assert templates_dir.exists()
    assert templates_dir.is_dir()

    # Check static directory
    static_dir = feature_dir / "static"
    assert static_dir.exists()
    assert static_dir.is_dir()


def test_create_feature_creates_python_files(tmp_project_dir):
    """Should create forms.py, models.py, and routes.py."""
    feature_name = "users"
    create_feature(feature_name)

    feature_dir = tmp_project_dir / feature_name

    forms_py = feature_dir / "forms.py"
    models_py = feature_dir / "models.py"
    routes_py = feature_dir / "routes.py"

    assert forms_py.exists()
    assert models_py.exists()
    assert routes_py.exists()


def test_create_feature_creates_template_files(tmp_project_dir):
    """Should create base.html and index.html templates."""
    feature_name = "users"
    create_feature(feature_name)

    templates_dir = tmp_project_dir / feature_name / "templates" / feature_name

    base_html = templates_dir / "base.html"
    index_html = templates_dir / "index.html"

    assert base_html.exists()
    assert index_html.exists()


def test_forms_py_has_pydantic_imports(tmp_project_dir):
    """forms.py should include Pydantic BaseModel and validators."""
    feature_name = "users"
    create_feature(feature_name)

    forms_py = tmp_project_dir / feature_name / "forms.py"
    content = forms_py.read_text()

    assert "from pydantic import BaseModel" in content
    assert "EmailStr" in content
    assert "Field" in content
    assert "field_validator" in content


def test_models_py_has_sqlalchemy_imports(tmp_project_dir):
    """models.py should include SQLAlchemy Column types and Base."""
    feature_name = "posts"
    create_feature(feature_name)

    models_py = tmp_project_dir / feature_name / "models.py"
    content = models_py.read_text()

    assert "from sqlalchemy import Column" in content
    assert "Integer" in content
    assert "String" in content
    assert "from core.database import Base" in content


def test_routes_py_has_fastapi_boilerplate(tmp_project_dir):
    """routes.py should define APIRouter with correct prefix and tags."""
    feature_name = "dashboard"
    create_feature(feature_name)

    routes_py = tmp_project_dir / feature_name / "routes.py"
    content = routes_py.read_text()

    assert "from fastapi import APIRouter" in content
    assert "Jinja2Templates" in content
    assert f'prefix="/{feature_name}"' in content
    assert f'tags=["{feature_name}"]' in content


def test_routes_py_has_root_endpoint(tmp_project_dir):
    """routes.py should define a root GET endpoint with template response."""
    feature_name = "blog"
    create_feature(feature_name)

    routes_py = tmp_project_dir / feature_name / "routes.py"
    content = routes_py.read_text()

    assert '@router.get("/", response_class=HTMLResponse)' in content
    assert "async def feature_root(request: Request):" in content
    assert "templates.TemplateResponse" in content
    assert f"Welcome to {feature_name}!" in content


def test_base_html_has_jinja_blocks(tmp_project_dir):
    """base.html should contain title and content blocks."""
    feature_name = "products"
    create_feature(feature_name)

    base_html = (
        tmp_project_dir / feature_name / "templates" / feature_name / "base.html"
    )
    content = base_html.read_text()

    assert "<!DOCTYPE html>" in content
    assert "{% block title %}" in content
    assert "{% endblock %}" in content
    assert "{% block content %}" in content


def test_index_html_extends_base(tmp_project_dir):
    """index.html should extend base.html and use Jinja variables."""
    feature_name = "products"
    create_feature(feature_name)

    index_html = (
        tmp_project_dir / feature_name / "templates" / feature_name / "index.html"
    )
    content = index_html.read_text()

    assert '{% extends "base.html" %}' in content
    assert "{% block content %}" in content
    assert "{{ msg }}" in content


def test_create_feature_is_idempotent(tmp_project_dir):
    """Running create_feature twice should not raise errors."""
    feature_name = "users"

    # First creation
    create_feature(feature_name)
    forms_py = tmp_project_dir / feature_name / "forms.py"
    first_content = forms_py.read_text()

    # Second creation (should overwrite)
    create_feature(feature_name)
    second_content = forms_py.read_text()

    assert first_content == second_content


# ---------------------------------------------------------
#  TESTS FOR inject_feature_to_main()
# ---------------------------------------------------------


def test_inject_feature_adds_import(tmp_project_dir):
    """Should add feature routes import to main.py."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text("from fastapi import FastAPI\n\napp = FastAPI()\n")

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()
    assert f"import {feature_name}.routes as {feature_name}_routes" in content


def test_inject_feature_adds_static_mount(tmp_project_dir):
    """Should add static file mount for the feature."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text(
        "from fastapi import FastAPI\n"
        "from fastapi.staticfiles import StaticFiles\n\n"
        "app = FastAPI()\n"
    )

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()
    assert f"app.mount('/static/{feature_name}'" in content
    assert f"directory='{feature_name}/static'" in content
    assert f"name='{feature_name}_static'" in content


def test_inject_feature_adds_router(tmp_project_dir):
    """Should add router include for the feature."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text("from fastapi import FastAPI\n\napp = FastAPI()\n")

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()
    assert f"app.include_router({feature_name}_routes.router)" in content


def test_inject_feature_maintains_order(tmp_project_dir):
    """Import should come before mount, mount before router."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text(
        "from fastapi import FastAPI\n"
        "from fastapi.staticfiles import StaticFiles\n\n"
        "app = FastAPI()\n"
    )

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()

    import_idx = content.index(f"import {feature_name}.routes")
    mount_idx = content.index(f"app.mount('/static/{feature_name}'")
    router_idx = content.index(f"app.include_router({feature_name}_routes.router)")

    assert import_idx < mount_idx < router_idx


def test_inject_feature_does_not_duplicate(tmp_project_dir):
    """Running inject twice should not duplicate code."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text("from fastapi import FastAPI\n\napp = FastAPI()\n")

    feature_name = "blog"

    # Inject twice
    inject_feature_to_main(app_dir, feature_name)
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()

    # Each line should appear exactly once
    assert content.count(f"import {feature_name}.routes") == 1
    assert content.count(f"app.mount('/static/{feature_name}'") == 1
    assert content.count(f"app.include_router({feature_name}_routes.router)") == 1


def test_inject_feature_handles_existing_mounts(tmp_project_dir):
    """Should add new mount after existing mounts."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text(
        "from fastapi import FastAPI\n"
        "from fastapi.staticfiles import StaticFiles\n\n"
        "app = FastAPI()\n"
        "app.mount('/static', StaticFiles(directory='static'), name='static')\n"
    )

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()
    lines = content.split("\n")

    # Find line indices
    static_general_idx = next(
        i for i, line in enumerate(lines) if "app.mount('/static'" in line
    )
    static_feature_idx = next(
        i
        for i, line in enumerate(lines)
        if f"app.mount('/static/{feature_name}'" in line
    )

    # Feature mount should come after general mount
    assert static_feature_idx > static_general_idx


def test_inject_feature_handles_existing_routers(tmp_project_dir):
    """Should add new router after existing routers."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text(
        "from fastapi import FastAPI\n"
        "import auth.routes as auth_routes\n\n"
        "app = FastAPI()\n"
        "app.include_router(auth_routes.router)\n"
    )

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()
    lines = content.split("\n")

    # Find router line indices
    auth_router_idx = next(
        i for i, line in enumerate(lines) if "auth_routes.router" in line
    )
    users_router_idx = next(
        i for i, line in enumerate(lines) if f"{feature_name}_routes.router" in line
    )

    # New router should come after existing router
    assert users_router_idx > auth_router_idx


def test_inject_feature_collapses_excessive_blank_lines(tmp_project_dir):
    """Should reduce more than 2 consecutive blank lines to 2."""
    app_dir = tmp_project_dir / "demoapp"
    app_dir.mkdir()
    main_py = app_dir / "main.py"

    main_py.write_text("from fastapi import FastAPI\n\n\n\napp = FastAPI()\n")

    feature_name = "users"
    inject_feature_to_main(app_dir, feature_name)

    content = main_py.read_text()

    # Should not have 3+ consecutive newlines
    assert "\n\n\n" not in content
