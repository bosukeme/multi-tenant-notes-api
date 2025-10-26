from fastapi import APIRouter, status, Request
from beanie import PydanticObjectId
from src.users.schemas import UserCreateSchema, UserReadSchema
from src.users.services import user_svc

user_router = APIRouter()


@user_router.post("/", response_model=UserReadSchema,
                  status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, org_id: PydanticObjectId,
                      payload: UserCreateSchema):
    return await user_svc.create_user(org_id, payload)


@user_router.get("/", response_model=list[UserReadSchema],
                 status_code=status.HTTP_200_OK)
async def list_users(request: Request, org_id: PydanticObjectId):
    return await user_svc.list_users(org_id)
