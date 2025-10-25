from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.connection import init_db
from src.organizations.routes import org_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    client = await init_db(app)
    yield
    print("Server has stopped!!!")
    client.close()


def register_routers(app: FastAPI) -> None:

    app.include_router(org_router, prefix="/organizations",
                       tags=["Organizations"])


def create_app() -> FastAPI:

    app = FastAPI(
        title="Multi-tenant Notes API",
        lifespan=life_span
    )

    register_routers(app)

    return app


app = create_app()
