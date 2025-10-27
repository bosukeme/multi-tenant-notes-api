from fastapi import Header
from src.organizations.models import Organization
from src.users.models import User
from beanie import PydanticObjectId

from src.utils.link_resolver import BaseService
from src.middlewares.errors import (
    MissingHeaders, OrganizationOrUserNotFound, UserDoesNotBelongToOrganization
    )


class TenantContext(BaseService):

    async def __call__(
        self,
        x_org_id: str = Header(None),
        x_user_id: str = Header(None)
    ):
        if not x_org_id or not x_user_id:
            raise MissingHeaders()

        org = await Organization.get(PydanticObjectId(x_org_id))
        user = await User.get(PydanticObjectId(x_user_id))

        if not org or not user:
            raise OrganizationOrUserNotFound()

        user_org = await self.resolve_link(user.org)

        if str(user_org.id) != str(org.id):
            raise UserDoesNotBelongToOrganization()

        return {"org": org, "user": user}
