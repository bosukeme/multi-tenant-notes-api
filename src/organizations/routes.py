from fastapi import APIRouter, status, Request
from src.organizations.schemas import (
    OrganizationCreateSchema, OrganizationReadSchema
)
from src.organizations.services import org_svc


org_router = APIRouter()


@org_router.post("/", response_model=OrganizationReadSchema,
                 status_code=status.HTTP_201_CREATED)
async def create_organization(request: Request,
                              data: OrganizationCreateSchema):
    return await org_svc.create_organization(data)


@org_router.get("/", response_model=list[OrganizationReadSchema],
                status_code=status.HTTP_200_OK)
async def list_organizations(request: Request,):
    return await org_svc.list_organizations()
