from fastapi import HTTPException, status
from src.organizations.models import Organization
from src.organizations.schemas import (
    OrganizationCreateSchema, OrganizationReadSchema
)


class OrganizationService:

    async def get_organization_by_name(self, name: str) -> Organization:
        existing = await Organization.find_one(Organization.name == name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization '{name}' already exists."
            )
        return None

    async def create_organization(
            self,
            data: OrganizationCreateSchema) -> Organization:

        existing = await self.get_organization_by_name(data.name)

        if not existing:
            org = Organization(**data.model_dump())
            await org.insert()
            return OrganizationReadSchema.from_mongo(org)

    async def list_organizations(self) -> list[Organization]:
        orgs = await Organization.find_all().to_list()
        return [
            OrganizationReadSchema.from_mongo(org) for org in orgs
        ]


org_svc = OrganizationService()
