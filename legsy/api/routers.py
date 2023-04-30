from fastapi import APIRouter

from legsy.api.routes import good_router

main_router = APIRouter()

main_router.include_router(
    good_router,
    prefix='/goods',
    tags=['Goods',],
)
