from aopi_index_builder import PackageIndex

from aopi_python.ctx import context
from aopi_python.models import models_list
from aopi_python.roles import RolesEnum
from aopi_python.routes import main_router


def main() -> PackageIndex:
    print(context)
    return PackageIndex(
        router=main_router,
        target_language="python",
        db_models=models_list,
        roles=RolesEnum,
        help=f"To use it add <aopi-url>{context.prefix}/simple as your index-url",
    )
