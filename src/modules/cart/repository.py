from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_

from src.core.repository import BaseRepo
from src.modules.cart.models import CartModel

class CartRepo(BaseRepo[CartModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, CartModel)

    async def get_by_user(self, user_id: int) -> Sequence[CartModel]:
        query = (
            select(CartModel)
            .where(CartModel.user_id == user_id)
            .options(selectinload(CartModel.product))
        )

        cart_items = await self.session.execute(query)
        return cart_items.scalars().all()

    async def get_by_id_and_user(self, user_id: int, item_id: int) -> CartModel | None:
        query = (
            select(CartModel)
            .where(
                and_(
                    CartModel.user_id == user_id,
                    CartModel.id == item_id
                )
            )
            .options(selectinload(CartModel.product))
        )
        cart_item = await self.session.execute(query)
        return cart_item.scalar_one_or_none()

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> CartModel | None:
        query = select(CartModel).where(
            and_(
                CartModel.user_id == user_id,
                CartModel.product_id == product_id
            )
        )
        cart_item = await self.session.execute(query)
        return cart_item.scalar_one_or_none()
    
    async def delete_all(self, cart_items: list[CartModel]):
        for i in cart_items:
            await self.session.delete(i)
        