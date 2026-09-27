from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import (
    hash_password,
    verify_password,
)


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "register.html",
        {
            "error": None
        }
    )


@router.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    email = email.strip().lower()

    if len(password) < 8:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error":
                "Password must be at least 8 characters."
            },
            status_code=400
        )

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error":
                "An account with this email already exists."
            },
            status_code=400
        )

    user = User(
        name=name.strip(),
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    request.session["user_id"] = user.id

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "error": None
        }
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.email ==
            email.strip().lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            password,
            user.hashed_password
        )
    ):

        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "error":
                "Invalid email or password."
            },
            status_code=401
        )

    request.session["user_id"] = user.id

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


@router.post("/logout")
def logout(
    request: Request
):

    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=303
    )