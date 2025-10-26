from fastapi import Depends, HTTPException, status
from typing import Literal
from src.dependencies.tenant import TenantContext

tenant_ctx = TenantContext()


Role = Literal["reader", "writer", "admin"]


def require_role(*allowed_roles: Role):
    async def role_checker(ctx=Depends(tenant_ctx)):
        user = ctx["user"]
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Role '{user.role}' not allowed."
            )
        return ctx
    return role_checker
