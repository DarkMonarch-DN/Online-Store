from fastapi import APIRouter

from src.modules.admin.products.router import router as products_router
from src.modules.admin.users.router import router as users_router
from src.modules.admin.orders.router import router as order_router


router = APIRouter()

router.include_router(
    router=products_router,
    prefix="/products",
)

router.include_router(
    router=users_router,
    prefix="/users",
)

router.include_router(
    router=order_router,
    prefix="/orders",
)