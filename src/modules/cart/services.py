
from fastapi import HTTPException, status

from src.modules.products.repository import ProductRepo
from src.modules.users.models import UserModel
from src.modules.cart.repository import CartRepo
from src.modules.cart.schemas import CartItemCreateScheme, CartItemUpdateScheme


class CartService:
    def __init__(self, cart_item_repo: CartRepo, product_repo: ProductRepo) -> None:
        self.cart_item_repo = cart_item_repo
        self.product_repo = product_repo

    async def get_cart_items(self, current_user: UserModel):
        cart_items = await self.cart_item_repo.get_by_user(current_user.id)
        return cart_items
    
    async def delete_all_cart_items(self, current_user: UserModel):
        cart_items = await self.cart_item_repo.get_by_user(current_user.id)
        await self.cart_item_repo.delete_all(list(cart_items))
        await self.cart_item_repo.commit()

    async def create_cart_item(self, 
        cart_item_data: CartItemCreateScheme,
        current_user: UserModel
    ):
        product = await self.product_repo.get(cart_item_data.product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        cart_item = await self.cart_item_repo.get_by_user_and_product(
            current_user.id,
            cart_item_data.product_id
        )
        if cart_item:
            cart_item.quantity += cart_item_data.quantity
        else:
            cart_item = await self.cart_item_repo.create(
                user_id=current_user.id,
                product_id=cart_item_data.product_id,
                quantity=cart_item_data.quantity
            )
        await self.cart_item_repo.commit()
        return cart_item, product

    async def update_quantity(self, current_user: UserModel, item_id: int, cart_item_data: CartItemUpdateScheme):
        cart_item = await self.cart_item_repo.get_by_id_and_user(
            current_user.id,
            item_id
        )
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        if cart_item.quantity + cart_item_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The quantity of goods cannot be negative."
            )

        cart_item.quantity += cart_item_data.quantity
        await self.cart_item_repo.commit()
        return cart_item
    
    async def delete_cart_item(self, current_user: UserModel, item_id: int) -> None:
        cart_item = await self.cart_item_repo.get_by_id_and_user(
            current_user.id,
            item_id
        )
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        await self.cart_item_repo.delete(cart_item)
        await self.cart_item_repo.commit()