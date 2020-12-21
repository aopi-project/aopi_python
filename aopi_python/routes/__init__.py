from fastapi import APIRouter

from aopi_python.routes.file_router import file_router
from aopi_python.routes.simple import simple_router

main_router = APIRouter()

main_router.include_router(simple_router)
main_router.include_router(file_router)
