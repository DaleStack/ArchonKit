**Sample Auth Flow**

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