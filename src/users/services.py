from beanie import PydanticObjectId
from src.users.models import User
from src.users.schemas import UserCreateSchema, UserReadSchema
from src.organizations.models import Organization

from src.middlewares.errors import OrganizationNotFound, UserAlreadyExists


class UserService:

    async def get_organization(self, org_id):
        org_id = PydanticObjectId(org_id)
        org = await Organization.get(org_id)
        if not org:
            raise OrganizationNotFound()
        return org

    async def create_user(self, org_id: PydanticObjectId,
                          data: UserCreateSchema) -> UserReadSchema:

        org = await self.get_organization(org_id)

        existing = await User.find_one({
            "email": data.email,
            "org.$id": org.id
        })
        if existing:
            raise UserAlreadyExists()

        user = User(**data.model_dump(), org=org)
        await user.insert()
        return await UserReadSchema.from_mongo(user)

    async def list_users(self, org_id: PydanticObjectId) -> list[User]:
        org = await self.get_organization(org_id)

        users = await (User.find({"org.$id": org.id})
                       .to_list())

        return [await UserReadSchema.from_mongo(user) for user in users]


user_svc = UserService()
