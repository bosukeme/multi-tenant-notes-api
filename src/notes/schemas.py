from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from beanie import Link

from src.organizations.schemas import OrganizationMiniSchema
from src.organizations.models import Organization

from src.users.schemas import UserMiniSchema
from src.users.models import User


class NoteCreateSchema(BaseModel):
    title: str
    content: str


class NoteReadSchema(BaseModel):
    id: str = Field(alias="_id", example="652c1e6fcf9b7f001f3f5a2b")
    title: str
    content: str
    created_at: datetime
    org: OrganizationMiniSchema
    author: UserMiniSchema

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    async def from_mongo(cls, note):
        if isinstance(note, dict):
            data = note.copy()
        else:
            data = note.model_dump(by_alias=True)

        if "_id" in data:
            data["_id"] = str(data["_id"])

        org_attr = getattr(note, "org", None)

        if org_attr:
            if isinstance(org_attr, Organization):
                org_doc = org_attr
            elif isinstance(org_attr, Link):
                org_doc = await org_attr.fetch()
            else:
                org_doc = None

            if org_doc:
                data["org"] = OrganizationMiniSchema(
                    id=str(org_doc.id),
                    name=org_doc.name,
                    description=org_doc.description
                )

        author_attr = getattr(note, "author", None)

        if author_attr:
            if isinstance(author_attr, User):
                author_doc = author_attr
            elif isinstance(author_attr, Link):
                author_doc = await author_attr.fetch()
            else:
                author_doc = None

            if author_doc:
                data["author"] = UserMiniSchema(
                    id=str(author_doc.id),
                    email=author_doc.email,
                    full_name=author_doc.full_name,
                    role=author_doc.role,
                )

        return cls(**data)
