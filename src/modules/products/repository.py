from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc, func

from src.core.repository import BaseRepo
from src.modules.products.models import ProductModel


class ProductRepo(BaseRepo[ProductModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProductModel)
    
    async def get_all(self, 
        limit: int, 
        offset: int, 
        sort_by: str, 
        order: str,
        min_price: float | None = None,
        max_price: float | None = None,
        categories: list[str] | None = None,
        search: str | None = None
    ) -> tuple[Sequence[ProductModel], int]:
        query = select(
            ProductModel, 
            func.count().over().label("total_count")
        ) 
        if categories is not None:
            query = query.where(ProductModel.categories.op("&&")(categories))
        if min_price is not None:
            query = query.where(ProductModel.price >= min_price)
        if max_price is not None:
            query = query.where(ProductModel.price <= max_price)
        if search is not None:
            query = query.where(ProductModel.title.ilike(f"%{search}%"))

        column = getattr(ProductModel, sort_by, None)
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
        
        products = [row[0] for row in rows]
        total = rows[0][1]

        return products, total
        