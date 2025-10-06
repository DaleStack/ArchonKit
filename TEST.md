**Sample Auth Flow**

`config.py`
```python
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: str = os.getenv("DEBUG")
    LOGIN_URL: str = os.getenv("LOGIN_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

```

`models.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
```

`forms.py`
```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class SignupForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("username")
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be blank")
        return value

class LoginForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
```


`routes.py`
```python
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .models import User
from core.utils import (
    set_csrf_token_in_session, validate_csrf_token, hash_password,
    verify_password, regenerate_session
)
from .forms import SignupForm, LoginForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.decorators import login_required

templates = Jinja2Templates(directory="users/templates/users")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    csrf_token = set_csrf_token_in_session(request)
    return templates.TemplateResponse("signup.html", {"request": request, "csrf_token": csrf_token})

@router.post("/signup", response_class=HTMLResponse)
async def signup_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    if not validate_csrf_token(request, csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    form = SignupForm(username=username, email=email, password=password)
    if db.query(User).filter(User.username == form.username).first() or db.query(User).filter(User.email == form.email).first():
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username or Email taken", "csrf_token": csrf_token})
    hashed_pw = hash_password(form.password)
    user = User(username=form.username, email=form.email, hashed_password=hashed_pw, is_active=True)
    db.add(user)
    db.commit()
    regenerate_session(request, user_id=user.id)
    return RedirectResponse("/users/profile", status_code=302)

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    csrf_token = set_csrf_token_in_session(request)
    return templates.TemplateResponse("login.html", {"request": request, "csrf_token": csrf_token})

@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    if not validate_csrf_token(request, csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    form = LoginForm(username=username, password=password)
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials", "csrf_token": csrf_token})
    regenerate_session(request, user_id=user.id)
    return RedirectResponse("/users/profile", status_code=302)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    response = RedirectResponse("/users/login", status_code=302)
    response.delete_cookie("session")
    return response

@router.get("/profile", response_class=HTMLResponse)
@login_required
async def profile(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.state.user_id
    user = db.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})
```

`signup.html`
```HTML
{% extends "base.html" %}
{% block content %}
<h2>Signup</h2>
<form method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <label>Username: <input name="username" required></label><br>
  <label>Email: <input name="email" required type="email"></label><br>
  <label>Password: <input name="password" required type="password"></label><br>
  <button type="submit">Sign Up</button>
</form>
{% if error %}<div style="color:red;">{{ error }}</div>{% endif %}
{% endblock %}

```

`login.html`
```HTML
{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="post">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <label>Username: <input name="username" required></label><br>
  <label>Password: <input name="password" required type="password"></label><br>
  <button type="submit">Login</button>
</form>
{% if error %}<div style="color:red;">{{ error }}</div>{% endif %}
{% endblock %}

```

`profile.html`
```HTML
{% extends "base.html" %}
{% block content %}
  <h2>Welcome, {{ user.username }}!</h2>
  <p>Email: {{ user.email }}</p>
  <a href="/users/logout">Log out</a>
{% endblock %}

```