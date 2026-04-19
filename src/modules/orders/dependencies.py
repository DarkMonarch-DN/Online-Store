from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.database import get_async_session
from src.modules.orders.repository import OrderRepo
from src.modules.orders.services import OrderService
from src.modules.cart.dependencies import CartRepoDep


def get_order_repo(session: AsyncSession = Depends(get_async_session)) -> OrderRepo:
    return OrderRepo(session)

OrderRepoDep = Annotated[OrderRepo, Depends(get_order_repo)]

def get_order_service(order_repo: OrderRepoDep, cart_repo: CartRepoDep) -> OrderService:
    return OrderService(order_repo, cart_repo)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]