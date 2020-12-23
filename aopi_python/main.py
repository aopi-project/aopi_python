from aopi_index_builder import PackageIndex

from aopi_python.ctx import context
from aopi_python.models import models_list
from aopi_python.routes import main_router


def main() -> PackageIndex:
    print(context)
    return PackageIndex(
        router=main_router,
        models=models_list,
        help="To use it add <aopi-url>/python/simple as your index-url",
    )
