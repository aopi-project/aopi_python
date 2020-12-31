from typing import Awaitable, Callable, Optional

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request

from aopi_python.ctx import context
from aopi_python.roles import RolesEnum

if context.enable_users:
    security = HTTPBasic()
else:

    async def security(_request: Request) -> None:
        return None


def get_user_with_role(
    role: RolesEnum,
) -> Callable[[Optional[HTTPBasicCredentials]], Awaitable[Optional[int]]]:
    async def route_security(
        credentials: Optional[HTTPBasicCredentials] = Depends(security),
    ) -> Optional[int]:
        if credentials is None:
            return None
        user_id = await context.get_user_id(credentials.username, credentials.password)
        await context.has_permission(user_id, role)
        return user_id

    return route_security
