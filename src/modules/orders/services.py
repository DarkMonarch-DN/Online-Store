from fastapi import HTTPException, status

from src.modules.orders.repository import OrderRepo
from src.modules.cart.repository import CartRepo
from src.modules.users.models import UserModel
from src.modules.orders.schemas import OrderCreateSchema, RequestOrderMeta, AdminOrderUpdateSchema


class OrderService:
    def __init__(self, order_repo: OrderRepo, cart_repo: CartRepo) -> None:
        self.order_repo = order_repo
        self.cart_repo = cart_repo

    async def get_user_orders(self, user_id: int):
        return await self.order_repo.get_all_by_user(user_id)
    
    async def create_order(self, order_data: OrderCreateSchema, current_user: UserModel):
        cart_item = await self.cart_repo.get_by_id_and_user(
            current_user.id, 
            order_data.cart_item_id
        )
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        order = await self.order_repo.create(
            total_price=cart_item.quantity * cart_item.product.price,
            quantity=cart_item.quantity,
            price_at_moment=cart_item.product.price,
            delivery_address=order_data.delivery_address,
            user_id=current_user.id,
            product_id=cart_item.product_id
        )

        await self.cart_repo.delete(cart_item)
        await self.order_repo.commit()
        return order
    
    async def get_all_orders(self, params: RequestOrderMeta):
        limit = params.size
        offset = (params.page - 1) * limit

        orders, total = await self.order_repo.get_all(
            limit=limit,
            offset=offset,
            sort_by=params.sort_by,
            order=params.order,
            status=params.status,
            min_price=params.min_total_price,
            max_price=params.max_total_price
        )
        return orders, total
    
    async def get_order_by_id(self, order_id: int):
        order = await self.order_repo.get(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order
    
    async def update_order(self, order_id: int, order_data: AdminOrderUpdateSchema):
        order = await self.get_order_by_id(order_id)

        new_order = await self.order_repo.update(
            order,
            **order_data.model_dump(exclude_unset=True)
        )
        return new_order
    
    async def delete_order(self, order_id: int) -> None:
        order = await self.get_order_by_id(order_id)
        await self.order_repo.delete(order)
        await self.order_repo.commit()