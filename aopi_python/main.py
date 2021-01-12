from aopi_index_builder import PackageIndex

from aopi_python.ctx import context
from aopi_python.index_functions import (
    find_packages_func,
    get_package_info_func,
    get_versions_func,
)
from aopi_python.models import models_list
from aopi_python.roles import RolesEnum
from aopi_python.routes import main_router


def main() -> PackageIndex:
    return PackageIndex(
        router=main_router,
        target_language="python",
        db_models=models_list,
        roles=RolesEnum,
        plugin_help=f"To use it add {{aopi-url}}/"
        f"{context.prefix}/simple as your index-url",
        find_packages_func=find_packages_func,
        get_package_info_func=get_package_info_func,
        get_versions_func=get_versions_func,
    )
