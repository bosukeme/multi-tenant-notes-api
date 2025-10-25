from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from src.core.config import Config


async def init_db(app: FastAPI) -> None:
    mongo_uri = Config.MONGO_URI
    client = AsyncIOMotorClient(mongo_uri)
    db = client[Config.DB_NAME]

    from src.organizations.models import Organization

    # docs = [Organization, User, Note]
    docs = [Organization]
    await init_beanie(database=db, document_models=docs)

    app.state.mongo_client = client
