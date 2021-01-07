from typing import Dict, List, Optional

from aopi_index_builder import FullPackageInfo, PackagePreview, PackageVersion

from aopi_python.ctx import context
from aopi_python.models import PythonPackage, PythonPackageVersion
from aopi_python.roles import RolesEnum


async def find_packages_func(
    user_id: Optional[int], pkg_name: str, limit: int, offset: int
) -> List[PackagePreview]:
    await context.has_permission(user_id=user_id, role=RolesEnum.read)

    def to_preview(package: Dict[str, str]) -> PackagePreview:
        return PackagePreview(
            id=package["id"], name=package["name"], short_description=package["summary"]
        )

    expr = PythonPackage.objects.filter(
        name__icontains=pkg_name
    ).build_select_expression()
    packages = await context.database.fetch_all(expr.limit(limit).offset(offset))
    return list(map(to_preview, packages))


async def get_package_info_func(user_id: Optional[int], pkg_id: int) -> FullPackageInfo:
    await context.has_permission(user_id=user_id, role=RolesEnum.read)
    package: PythonPackage = await PythonPackage.objects.get(id=pkg_id)
    last_version_query = PythonPackageVersion.objects.filter(
        package=package
    ).build_select_expression()
    last_version_query.order_by(
        PythonPackageVersion.__table__.c.upload_time.desc()
    ).limit(1)
    last_version = await context.database.fetch_one(last_version_query)
    description = None
    if "description" in last_version.keys():
        description = last_version["description"]
    return FullPackageInfo(
        id=package.id,
        name=package.name,
        short_description=package.summary,
        description=description,
        last_version=last_version["version"],
        metadata={
            key: val
            for key, val in package.items()
            if key not in ["id", "name", "summary", "description"]
        },
    )


async def get_versions_func(
    user_id: Optional[int], pkg_id: int
) -> List[PackageVersion]:
    await context.has_permission(user_id=user_id, role=RolesEnum.read)

    def to_package_version(version: PythonPackageVersion) -> PackageVersion:
        return PackageVersion(
            version=version.version,
            yanked=version.yanked,
            metadata={
                key: val
                for key, val in version.items()
                if key not in ["version", "yanked", "package"]
            },
        )

    versions = await PythonPackageVersion.objects.filter(package__id=pkg_id).all()

    return list(map(to_package_version, versions))
