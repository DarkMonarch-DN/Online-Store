from fastapi import APIRouter

from src.modules.users.router import router as user_router
from src.modules.products.router import router as product_router
from src.modules.cart.router import router as cart_router
from src.modules.orders.router import router as order_router
from src.modules.admin import router as admin_router

global_router = APIRouter(prefix="/v1")

global_router.include_router(
    router=user_router,
)

global_router.include_router(
    router=product_router,
    prefix="/products",
    tags=["Products"]
)

global_router.include_router(
    router=cart_router,
    prefix="/carts",
    tags=["Cart"]
)

global_router.include_router(
    router=order_router,
    prefix="/orders",
    tags=["Orders"]
)

global_router.include_router(
    router=admin_router,
    prefix="/admin",
    tags=["Admin"]
)
