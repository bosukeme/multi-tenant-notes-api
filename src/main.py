from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.connection import init_db
from src.middlewares import register_middleware
from src.organizations.routes import org_router
from src.users.routes import user_router
from src.notes.routes import note_router
from src.middlewares.rate_limit import apply_rate_limit_to_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    client = await init_db(app)
    try:
        yield
    finally:
        print("Server has stopped!!!")
        if client:
            client.close()


def register_routers(app: FastAPI) -> None:

    apply_rate_limit_to_router(org_router, "5/minute")
    app.include_router(org_router, prefix="/organizations",
                       tags=["Organizations"])

    apply_rate_limit_to_router(user_router, "5/minute")
    app.include_router(user_router, prefix="/organizations/{org_id}/users",
                       tags=["users"])

    apply_rate_limit_to_router(note_router, "5/minute")
    app.include_router(note_router, prefix="/notes",
                       tags=["notes"])


def create_app() -> FastAPI:

    app = FastAPI(
        title="Multi-tenant Notes API",
        lifespan=life_span,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/")
    async def home():
        return {"message": "Welcome to the Multi Tenant Notes API"}

    register_middleware(app)
    register_routers(app)

    return app


app = create_app()
