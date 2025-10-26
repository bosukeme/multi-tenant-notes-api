from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId
from beanie import Link
from src.organizations.schemas import OrganizationMiniSchema
from src.organizations.models import Organization


class UserCreateSchema(BaseModel):
    email: EmailStr
    full_name: str
    role: str = Field(default="reader", pattern="^(reader|writer|admin)$")


class UserReadSchema(BaseModel):
    id: str = Field(alias="_id", example="652c1e6fcf9b7f001f3f5a2b")
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime
    org: OrganizationMiniSchema

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    async def from_mongo(cls, user):
        if isinstance(user, dict):
            data = user.copy()
        else:
            data = user.model_dump(by_alias=True)

        if "_id" in data:
            data["_id"] = str(data["_id"])

        org_attr = getattr(user, "org", None)
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

        return cls(**data)
