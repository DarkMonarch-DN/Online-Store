from fastapi import APIRouter, Query

from src.core.schemas import ResponseWrapper, PaginatedResponse, ResponseMeta
from src.modules.users import CurrentAdminDep
from src.modules.orders import OrderServiceDep
from src.modules.orders.schemas import OrderReadSchema, AdminOrderUpdateSchema, RequestOrderMeta


router = APIRouter()

@router.get("/", 
    summary="Get all orders", 
    response_model=ResponseWrapper[
        PaginatedResponse[
            OrderReadSchema
        ]
    ]
)
async def get_all_orders(
    current_user: CurrentAdminDep,
    order_service: OrderServiceDep,
    params: RequestOrderMeta = Query()
):
    orders, total = await order_service.get_all_orders(
        params
    )

    return ResponseWrapper(
        data=PaginatedResponse(
            items=orders,
            meta=ResponseMeta(
                total=total,
                page=params.page,
                size=params.size,
                pages=total // params.size,
                sort_by=params.sort_by,
                order=params.order
            )
        ),
        message="Orders get success"
    )

@router.get("/{user_id}/users", summary="Get user orders", response_model=ResponseWrapper[list[OrderReadSchema]])
async def get_user_orders(
    user_id: int,
    current_user: CurrentAdminDep,
    order_service: OrderServiceDep
):
    orders = await order_service.get_user_orders(
        user_id
    )
    return ResponseWrapper(
        data=orders,
        message="Get user orders success"
    )

@router.get("/{order_id}", summary="Get order by id", response_model=ResponseWrapper[OrderReadSchema])
async def get_one_order(
    order_id: int,
    current_user: CurrentAdminDep,
    order_service: OrderServiceDep
):
    order = await order_service.get_order_by_id(order_id)
    return ResponseWrapper(
        data=order,
        message="Order get success"
    )

@router.patch("/{order_id}", summary="Update user order", response_model=ResponseWrapper[OrderReadSchema])
async def update_user_order(
    order_id: int,
    order_data: AdminOrderUpdateSchema,
    current_user: CurrentAdminDep,
    order_service: OrderServiceDep,
):
    order = await order_service.update_order(
        order_id,
        order_data
    )
    return ResponseWrapper(
        data=order,
        message="Order updated success"
    )

@router.delete("/", summary="Delete user order", response_model=ResponseWrapper)
async def delete_user_order(
    order_id: int,
    current_user: CurrentAdminDep,
    order_service: OrderServiceDep
):
    order = await order_service.delete_order(order_id)
    return ResponseWrapper(
        data=order,
        message="Order deleted success"
    )