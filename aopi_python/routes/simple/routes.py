import shutil
from operator import attrgetter, itemgetter
from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from natsort import natsorted
from orm import NoMatch
from sqlalchemy.sql import Select
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

from aopi_python import models
from aopi_python.ctx import context, plugin_prefix, templates
from aopi_python.models.dist_info import PackageUploadModel
from aopi_python.routes.simple.logic import save_file

simple_router = APIRouter()

PREFIX = f"{plugin_prefix}/simple"


@simple_router.get("", response_class=HTMLResponse)
async def python_simple_index_page(request: Request) -> templates.TemplateResponse:
    select: Select = sqlalchemy.sql.select([models.PythonPackage.objects.table.c.name])
    packages = map(itemgetter(0), await context.database.fetch_all(select))
    return templates.TemplateResponse(
        "simple/index.jinja2",
        {"prefix": PREFIX, "packages": packages, "request": request},
    )


@simple_router.post("")
async def upload_python_package(
    response: Response,
    upload: PackageUploadModel = Depends(PackageUploadModel.as_form),  # type: ignore
) -> Response:
    logger.debug(upload)
    pkg_dir = context.packages_dir / upload.name / upload.version / upload.filetype
    try:
        await models.PythonPackageVersion.objects.get(
            package__name=upload.name,
            version=upload.version,
            filetype=upload.filetype,
        )
        logger.debug(f"Failed to upload {upload.name}. Already exists.")
        raise HTTPException(status_code=409, detail="Distribution already exists.")
    except NoMatch:
        pass
    package_exists = await models.PythonPackage.objects.filter(
        name=upload.name
    ).exists()
    try:
        file_path = pkg_dir / upload.content.filename
        await save_file(file_path, upload.content)
        logger.debug(f"Saved package file {upload.name} {upload.filetype}")
        if package_exists:
            package = await models.PythonPackage.objects.get(name=upload.name)
            await package.update_by_dist_info(upload)
        else:
            package = await models.PythonPackage.create_by_dist_info(upload)
        await models.PythonPackageVersion.create_by_dist_info(
            filename=upload.content.filename,
            package=package,
            size=file_path.stat().st_size,
            dist_info=upload,
        )
    except Exception as e:
        logger.exception(e)
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)
        raise HTTPException(
            status_code=400, detail="Something went wrong during saving."
        )

    response.status_code = 201
    return response


@simple_router.get("/{pkg_name}/", response_class=HTMLResponse)
async def get_python_package_info(
    pkg_name: str, request: Request
) -> templates.TemplateResponse:
    """
    Get information about the package.

    """
    versions: List[
        models.PythonPackageVersion
    ] = await models.PythonPackageVersion.objects.filter(package__name=pkg_name).all()
    if not versions:
        raise HTTPException(status_code=404, detail="Package was not found")
    versions = natsorted(versions, key=attrgetter("version"))
    readme = str() if not versions else versions[-1].description
    return templates.TemplateResponse(
        "simple/package_versions.jinja2",
        {
            "request": request,
            "name": pkg_name,
            "prefix": PREFIX,
            "versions": versions,
            "readme": readme,
        },
    )
