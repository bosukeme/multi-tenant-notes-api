from datetime import datetime, timezone
from beanie import Document, Indexed
from pydantic import Field
from typing import Annotated


class Organization(Document):

    name: Annotated[str, Indexed(unique=True), Field(min_length=3)]
    description: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "organizations"
