from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.modules.cart.repository import CartRepo
from src.modules.cart.services import CartService
from src.modules.products import ProductRepoDep


def get_cart_repo(session: AsyncSession = Depends(get_async_session)) -> CartRepo:
    return CartRepo(session)

CartRepoDep = Annotated[CartRepo, Depends(get_cart_repo)]

def get_cart_service(
    product_repo: ProductRepoDep,
    cart_repo: CartRepo = Depends(get_cart_repo),
) -> CartService:
    return CartService(cart_repo, product_repo)

CartServiceDep = Annotated[CartService, Depends(get_cart_service)]