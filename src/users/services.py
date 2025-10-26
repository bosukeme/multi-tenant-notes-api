from fastapi import HTTPException, status
from beanie import PydanticObjectId
from src.users.models import User
from src.users.schemas import UserCreateSchema, UserReadSchema
from src.organizations.models import Organization


class UserService:

    async def get_organization(self, org_id):
        org_id = PydanticObjectId(org_id)
        org = await Organization.get(org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found")
        return org

    async def create_user(self, org_id: PydanticObjectId,
                          data: UserCreateSchema) -> UserReadSchema:

        org = await self.get_organization(org_id)

        existing = await User.find_one({
            "email": data.email,
            "org.$id": org.id
        })
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f"User with email '{data.email}' "
                        "already exists in this organization.")
            )

        user = User(**data.model_dump(), org=org)
        await user.insert()
        return await UserReadSchema.from_mongo(user)

    async def list_users(self, org_id: PydanticObjectId) -> list[User]:
        org = await self.get_organization(org_id)

        users = await (User.find({"org.$id": org.id})
                       .to_list())

        return [await UserReadSchema.from_mongo(user) for user in users]


user_svc = UserService()
