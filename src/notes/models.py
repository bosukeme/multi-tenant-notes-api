from datetime import datetime, timezone
from beanie import Document, Link
from pydantic import Field
from src.organizations.models import Organization
from src.users.models import User


class Note(Document):
    title: str
    content: str
    org: Link[Organization]
    author: Link[User]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "notes"
        fetch_links = True
