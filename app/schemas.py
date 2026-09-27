from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class RegisterSchema(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginSchema(BaseModel):

    email: EmailStr

    password: str


class HomePlannerSchema(BaseModel):

    total_budget: float = Field(
        gt=0
    )

    room_type: str = Field(
        min_length=2
    )

    room_size: str = Field(
        min_length=1
    )

    preferred_style: str = Field(
        min_length=2
    )

    color_preference: str = Field(
        min_length=2
    )

    number_of_items: int = Field(
        ge=1,
        le=100
    )

    additional_requirements: str = ""


class PartyPlannerSchema(BaseModel):

    total_budget: float = Field(
        gt=0
    )

    party_type: str = Field(
        min_length=2
    )

    guests: int = Field(
        ge=1,
        le=10000
    )

    venue_type: str = Field(
        min_length=2
    )

    theme: str = Field(
        min_length=2
    )

    food_preference: str = Field(
        min_length=2
    )

    decoration_preference: str = Field(
        min_length=2
    )

    additional_requirements: str = ""


class JewelryPlannerSchema(BaseModel):

    budget: float = Field(
        gt=0
    )

    jewelry_type: str = Field(
        min_length=2
    )

    occasion: str = Field(
        min_length=2
    )

    metal_preference: str = Field(
        min_length=2
    )

    style: str = Field(
        min_length=2
    )

    gender: str = Field(
        min_length=1
    )

    additional_requirements: str = ""


class RecommendationOut(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    planner_type: str

    recommendation_text: str

    created_at: str