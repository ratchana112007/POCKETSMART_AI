from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Recommendation


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "user": user
        }
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user
        }
    )


@router.get(
    "/planner/home",
    response_class=HTMLResponse
)
def home_planner(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "home_planner.html",
        {
            "user": user
        }
    )


@router.get(
    "/planner/party",
    response_class=HTMLResponse
)
def party_planner(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "party_planner.html",
        {
            "user": user
        }
    )


@router.get(
    "/planner/jewelry",
    response_class=HTMLResponse
)
def jewelry_planner(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "jewelry_planner.html",
        {
            "user": user
        }
    )


@router.get(
    "/recommendations",
    response_class=HTMLResponse
)
def recommendations_page(
    request: Request,
    user=Depends(get_current_user)
):

    return templates.TemplateResponse(
        request,
        "recommendations.html",
        {
            "user": user
        }
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
def history(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    recommendations = []

    if user:

        recommendations = (
            db.query(Recommendation)
            .filter(
                Recommendation.user_id == user.id
            )
            .order_by(
                Recommendation.created_at.desc()
            )
            .all()
        )

    return templates.TemplateResponse(
        request,
        "history.html",
        {
            "user": user,
            "recommendations": recommendations
        }
    )