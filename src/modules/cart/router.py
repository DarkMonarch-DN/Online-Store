from fastapi import APIRouter

from src.modules.users import CurrentUserDep
from src.modules.cart.schemas import CartItemReadScheme, CartItemCreateScheme, CartItemUpdateScheme
from src.modules.cart.dependencies import CartServiceDep
from src.core.schemas import ResponseWrapper

router = APIRouter()

# Cart
@router.get("/", summary="Get user cart", response_model=ResponseWrapper[list[CartItemReadScheme]])
async def get_user_cart(
    current_user: CurrentUserDep,
    cart_service: CartServiceDep,
):
    cart_items = await cart_service.get_cart_items(
        current_user
    )

    return ResponseWrapper(
        data=cart_items,
        message="Get cart item is success"
    )

@router.delete("/", summary="Clear cart", response_model=ResponseWrapper)
async def delete_cart(
    current_user: CurrentUserDep,
    cart_service: CartServiceDep,
):
    await cart_service.delete_all_cart_items(current_user)
    
    return ResponseWrapper(
        message="Cart success cleared"
    )


# Cart items
@router.post("/items", summary="Create cart item", response_model=ResponseWrapper[CartItemReadScheme])
async def create_cart_item(
    cart_item_data: CartItemCreateScheme,
    current_user: CurrentUserDep,
    cart_service: CartServiceDep,
):
    cart_item, product = await cart_service.create_cart_item(
        cart_item_data,
        current_user
    )
    return ResponseWrapper(
        data={
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "created_at": cart_item.created_at,
            "product": product
        },
        message="Success added product"
    )

@router.patch("/items/{item_id}", summary="Edit quantity", response_model=ResponseWrapper[CartItemReadScheme])
async def update_quantity(
    item_id: int, 
    cart_item_data: CartItemUpdateScheme,
    current_user: CurrentUserDep,
    cart_service: CartServiceDep,
):
    cart_item = await cart_service.update_quantity(
        current_user, 
        item_id, 
        cart_item_data
    )

    return ResponseWrapper(
        data=cart_item,
        message="Success updated quantity"
    )

@router.delete("/items/{item_id}", summary="Delete item", response_model=ResponseWrapper)
async def delete_cart_item(
    item_id: int, 
    current_user: CurrentUserDep,
    cart_service: CartServiceDep,
):
    await cart_service.delete_cart_item(current_user, item_id)

    return ResponseWrapper(
        message="Success deleted cart item"
    )

