import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.middlewares import register_middleware
from src.organizations.models import Organization
from src.users.models import User
from src.notes.models import Note

from src.organizations.routes import org_router
from src.users.routes import user_router
from src.notes.routes import note_router
from src.core.config import Config


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def app():
    app = FastAPI()

    register_middleware(app)

    app.include_router(org_router, prefix="/organizations",
                       tags=["Organizations"])
    app.include_router(user_router, prefix="/organizations/{org_id}/users",
                       tags=["users"])
    app.include_router(note_router, prefix="/notes",
                       tags=["notes"])

    client = AsyncIOMotorClient(Config.MONGO_URI)
    db = client["test_db"]

    await init_beanie(database=db, document_models=[Organization, User, Note])
    yield app

    await db.drop_collection("organizations")
    await db.drop_collection("users")
    await db.drop_collection("notes")
    client.close()


@pytest.fixture(autouse=True)
async def clear_db():

    await Organization.delete_all()
    await User.delete_all()
    await Note.delete_all()

    yield


@pytest.fixture
async def client(app: FastAPI):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,
                           base_url="http://testserver") as ac:
        yield ac
