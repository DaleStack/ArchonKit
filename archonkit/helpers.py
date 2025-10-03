import os

def create_app(app_name):
    os.makedirs(f"{app_name}/core", exist_ok=True)
    os.makedirs(f"{app_name}/templates", exist_ok=True)
    with open(f"{app_name}/templates/index.html", "w") as f:
        f.write("<h1>{{ msg }}</h1>")
    main_py_content = """
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "msg": "Welcome to ArchonKit!"})
    """.strip()
    with open(f"{app_name}/main.py", "w") as f:
        f.write(main_py_content)

def create_feature(feature_name):
    os.makedirs(feature_name, exist_ok=True)
    open(os.path.join(feature_name, "forms.py"), "a").close()
    open(os.path.join(feature_name, "models.py"), "a").close()
    open(os.path.join(feature_name, "routes.py"), "a").close()
    os.makedirs(os.path.join(feature_name, "templates"), exist_ok=True)
    os.makedirs(os.path.join(feature_name, "static"), exist_ok=True)
