from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

from src.organizations.schemas import OrganizationMiniSchema
from src.users.schemas import UserMiniSchema
from src.utils.link_resolver import BaseService

base_svc = BaseService()


class NoteCreateSchema(BaseModel):
    title: str
    content: str


class NoteReadSchema(BaseModel):
    id: str = Field(alias="_id", json_schema_extra={
                    "example": "652c1e6fcf9b7f001f3f5a2b"})
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
        org_doc = await base_svc.resolve_link(org_attr)

        if org_doc:
            data["org"] = OrganizationMiniSchema(
                id=str(org_doc.id),
                name=org_doc.name,
                description=org_doc.description
            )

        author_attr = getattr(note, "author", None)
        author_doc = await base_svc.resolve_link(author_attr)

        if author_doc:
            data["author"] = UserMiniSchema(
                id=str(author_doc.id),
                email=author_doc.email,
                full_name=author_doc.full_name,
                role=author_doc.role,
            )

        return cls(**data)
