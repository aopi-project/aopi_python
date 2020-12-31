from typing import Optional

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from aopi_python.ctx import context
from aopi_python.roles import RolesEnum
from aopi_python.routes.simple.dependencies import get_user_with_role

file_router = APIRouter()


@file_router.get("/python_files/{pkg_name}/{version}/{dist_type}/{filename}")
async def get_python_dist_file(
    pkg_name: str,
    version: str,
    dist_type: str,
    filename: str,
    _: Optional[int] = Depends(get_user_with_role(RolesEnum.read)),
) -> FileResponse:
    file_path = context.packages_dir / pkg_name / version / dist_type / filename
    return FileResponse(
        file_path,
        status_code=200,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
