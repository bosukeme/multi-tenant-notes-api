from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict


class OrganizationCreateSchema(BaseModel):
    name: str = Field(..., example="ABC Org")
    description: str | None = Field(None, example="The best Org.")


class OrganizationReadSchema(BaseModel):
    id: str = Field(alias="_id", example="652c1e6fcf9b7f001f3f5a2b")
    name: str
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    def from_mongo(cls, org):
        """Safely convert Mongo ObjectId -> str before validation"""
        if isinstance(org, dict):
            data = org.copy()
        else:
            data = org.model_dump(by_alias=True)

        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class OrganizationMiniSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str | None = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
