from fastapi import APIRouter

from src.core.schemas import ResponseWrapper
from src.modules.users import CurrentUserDep
from src.modules.orders.dependencies import OrderServiceDep
from src.modules.orders.schemas import OrderCreateSchema, OrderReadSchema

router = APIRouter()


@router.get("/", summary="Get user orders", response_model=ResponseWrapper[list[OrderReadSchema]])
async def get_orders(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
):
    orders = await order_service.get_user_orders(
        current_user.id
    )
    return ResponseWrapper(
        data=orders,
        message="Orders get success"
    )

@router.post("/", summary="Create new order", response_model=ResponseWrapper[OrderReadSchema])
async def create_order(
    order_data: OrderCreateSchema,
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
):
    order = await order_service.create_order(
        order_data,
        current_user
    )
    return ResponseWrapper(
        data=order,
        message="Order success created"
    )