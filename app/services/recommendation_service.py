import json

from sqlalchemy.orm import Session

from app.ai.gemini_service import (
    generate_recommendation,
)

from app.models import (
    Recommendation,
    User,
)

from app.services.catalog import CATALOG

from app.services.platform_links import (
    search_links,
)


def _fallback(
    planner_type: str,
    data: dict
) -> str:

    budget = data.get(
        "total_budget",
        data.get("budget", 0)
    )

    if planner_type == "home":

        allocation = (
            "Furniture 45%, "
            "lighting/decor 20%, "
            "storage 15%, "
            "soft furnishings 10%, "
            "contingency 10%."
        )

        categories = ", ".join(
            CATALOG["home"]["furniture"]
            + CATALOG["home"]["decor"]
        )

    elif planner_type == "party":

        allocation = (
            "Food 40%, "
            "venue 20%, "
            "decoration 15%, "
            "entertainment 10%, "
            "invitations/logistics 5%, "
            "contingency 10%."
        )

        categories = ", ".join(
            CATALOG["party"]["food"]
            + CATALOG["party"]["decoration"]
        )

    else:

        allocation = (
            "Jewelry item 70%, "
            "customization/gemstones 15%, "
            "care/packaging 5%, "
            "contingency 10%."
        )

        categories = ", ".join(
            CATALOG["jewelry"]["types"]
        )

    return (
        f"Budget: {budget:.2f}\n\n"

        f"Budget allocation:\n"
        f"{allocation}\n\n"

        f"Suggested categories:\n"
        f"{categories}\n\n"

        "Practical tips:\n"

        "- Compare specifications, warranty/"
        "return terms, and total cost before buying.\n"

        "- Treat external links as search links; "
        "availability and prices must be verified by the user.\n"

        "- Keep the contingency amount uncommitted "
        "until the main requirements are covered."
    )


def create_recommendation(
    db: Session,
    user: User,
    planner_type: str,
    data: dict
) -> Recommendation:

    text = (
        generate_recommendation(
            planner_type,
            data
        )
        or
        _fallback(
            planner_type,
            data
        )
    )

    recommendation = Recommendation(

        user_id=user.id,

        planner_type=planner_type,

        input_data=json.dumps(
            data
        ),

        recommendation_text=text,
    )

    db.add(recommendation)

    db.commit()

    db.refresh(
        recommendation
    )

    return recommendation


def get_links(
    planner_type: str,
    data: dict
) -> list[dict]:

    if planner_type == "home":

        query = (
            f"{data.get('room_type')} "
            f"{data.get('preferred_style')} "
            "furniture decor"
        )

    elif planner_type == "party":

        query = (
            f"{data.get('party_type')} "
            "party "
            f"{data.get('theme')} "
            "decoration"
        )

    else:

        query = (
            f"{data.get('jewelry_type')} "
            f"{data.get('style')} "
            f"{data.get('metal_preference')}"
        )

    return search_links(
        query
    )