from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_user
from app.models import User
from app.schemas import (
    HomePlannerSchema,
    PartyPlannerSchema,
    JewelryPlannerSchema,
)
from app.services.recommendation_service import (
    create_recommendation,
    get_links,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


async def get_request_data(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        return await request.json()

    form = await request.form()
    return dict(form)


@router.post("/home")
async def home_recommendation(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    raw_data = await get_request_data(request)

    data = HomePlannerSchema.model_validate(raw_data)

    recommendation = create_recommendation(
        db=db,
        user=user,
        planner_type="home",
        data=data.model_dump(),
    )

    return {
        "id": recommendation.id,
        "planner_type": recommendation.planner_type,
        "recommendation": recommendation.recommendation_text,
        "shopping_links": get_links(
            "home",
            data.model_dump(),
        ),
    }


@router.post("/party")
async def party_recommendation(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    raw_data = await get_request_data(request)

    data = PartyPlannerSchema.model_validate(raw_data)

    recommendation = create_recommendation(
        db=db,
        user=user,
        planner_type="party",
        data=data.model_dump(),
    )

    return {
        "id": recommendation.id,
        "planner_type": recommendation.planner_type,
        "recommendation": recommendation.recommendation_text,
        "shopping_links": get_links(
            "party",
            data.model_dump(),
        ),
    }


@router.post("/jewelry")
async def jewelry_recommendation(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    raw_data = await get_request_data(request)

    data = JewelryPlannerSchema.model_validate(raw_data)

    recommendation = create_recommendation(
        db=db,
        user=user,
        planner_type="jewelry",
        data=data.model_dump(),
    )

    return {
        "id": recommendation.id,
        "planner_type": recommendation.planner_type,
        "recommendation": recommendation.recommendation_text,
        "shopping_links": get_links(
            "jewelry",
            data.model_dump(),
        ),
    }