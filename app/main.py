from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import create_tables
from app.routes import auth
from app.routes import pages
from app.routes import recommendations


app = FastAPI(
    title="PocketSmart AI",
    description="Smart budget and recommendation assistant",
    version="1.0.0"
)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


create_tables()


app.include_router(
    pages.router
)
app.include_router(
    recommendations.router
)
app.include_router(
    auth.router
)