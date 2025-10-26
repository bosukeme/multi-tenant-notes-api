from fastapi import Header, HTTPException, status
from src.organizations.models import Organization
from src.users.models import User
from beanie import PydanticObjectId

from src.utils.link_resolver import BaseService


class TenantContext(BaseService):

    async def __call__(
        self,
        x_org_id: str = Header(None),
        x_user_id: str = Header(None)
    ):
        if not x_org_id or not x_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing X-Org-ID or X-User-ID headers"
            )

        org = await Organization.get(PydanticObjectId(x_org_id))
        user = await User.get(PydanticObjectId(x_user_id))

        if not org or not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization or User not found"
            )

        user_org = await self.resolve_link(user.org)

        if str(user_org.id) != str(org.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=("User does not belong to this organization")
            )

        return {"org": org, "user": user}
