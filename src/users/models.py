from typing import Annotated
from datetime import datetime, timezone
from beanie import Document, Link, Indexed
from pydantic import EmailStr, Field
from src.organizations.models import Organization


class User(Document):

    email: Annotated[EmailStr, Indexed(unique=True)]
    full_name: str
    role: str = Field(default="reader", description="reader | writer | admin")
    org: Link[Organization]
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "users"
        fetch_links = True
