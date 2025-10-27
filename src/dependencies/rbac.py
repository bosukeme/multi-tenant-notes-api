from fastapi import Depends
from typing import Literal
from src.dependencies.tenant import TenantContext
from src.middlewares.errors import InvalidRoleAccess

tenant_ctx = TenantContext()


Role = Literal["reader", "writer", "admin"]


def require_role(*allowed_roles: Role):
    async def role_checker(ctx=Depends(tenant_ctx)):
        user = ctx["user"]
        if user.role not in allowed_roles:
            raise InvalidRoleAccess()
        return ctx
    return role_checker
