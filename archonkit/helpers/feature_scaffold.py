import os


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
    with open(
        os.path.join(feature_name, "templates", feature_name, "base.html"), "w"
    ) as f:
        f.write(base_html)

    # Boilerplate index.html extending base.html
    index_html = """{% extends "base.html" %}
{% block content %}
<h1>{{ msg }}</h1>
{% endblock %}
"""
    with open(
        os.path.join(feature_name, "templates", feature_name, "index.html"), "w"
    ) as f:
        f.write(index_html)


def inject_feature_to_main(app_dir, feature_name):
    main_py = os.path.join(app_dir, "main.py")

    import_line = f"import {feature_name}.routes as {feature_name}_routes\n"
    static_line = f"app.mount('/static/{feature_name}', StaticFiles(directory='{feature_name}/static'), name='{feature_name}_static')\n"
    router_line = f"app.include_router({feature_name}_routes.router)\n"

    with open(main_py, "r") as f:
        lines = f.readlines()

    # Insert import_line after the last import
    last_import = max(
        i
        for i, line in enumerate(lines)
        if line.strip().startswith(("import ", "from "))
    )
    if import_line not in lines:
        lines.insert(last_import + 1, import_line)

    # Insert static_line after the last app.mount (or after app = FastAPI())
    mount_indices = [
        i for i, line in enumerate(lines) if line.strip().startswith("app.mount")
    ]
    mount_insert_idx = (
        mount_indices[-1] + 1
        if mount_indices
        else next(i for i, line in enumerate(lines) if "app = FastAPI()" in line) + 1
    )
    if static_line not in lines:
        lines.insert(mount_insert_idx, static_line)

    # Insert router_line after the last app.include_router (or after last mount)
    router_indices = [
        i
        for i, line in enumerate(lines)
        if line.strip().startswith("app.include_router")
    ]
    router_insert_idx = (
        router_indices[-1] + 1 if router_indices else mount_insert_idx + 1
    )
    if router_line not in lines:
        lines.insert(router_insert_idx, router_line)

    # Deduplicate blank lines (optional: collapse >2 blank lines)
    code = "".join(lines)
    while "\n\n\n" in code:
        code = code.replace("\n\n\n", "\n\n")
    with open(main_py, "w") as f:
        f.write(code)
