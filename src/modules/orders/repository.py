from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func

from src.core.repository import BaseRepo
from src.modules.orders.models import OrderModel, OrderStatus


class OrderRepo(BaseRepo[OrderModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrderModel)

    async def get_all_by_user(self, user_id: int) -> Sequence[OrderModel]:
        orders = await self.session.execute(
            select(OrderModel).where(OrderModel.user_id == user_id)
        )
        return orders.scalars().all()
    
    async def get_all(self, 
        limit: int, 
        offset: int, 
        sort_by: str, 
        order: str,
        status: OrderStatus | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> tuple[Sequence[OrderModel], int]:
        query = select(
            OrderModel, 
            func.count().over().label("total_count")
        )

        if status is not None:
            query = query.where(OrderModel.status == status)

        if min_price is not None:
            query = query.where(OrderModel.total_price >= min_price)
        if max_price is not None:
            query = query.where(OrderModel.total_price <= max_price)

        column = getattr(OrderModel, sort_by, None)
        if column:
            order_fun = desc if order == "desc" else asc
            query = query.order_by(order_fun(column))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(query)
        rows = result.all()
        if not rows:
            return [], 0
        
        orders = [row[0] for row in rows]
        total = rows[0][1]

        return orders, total