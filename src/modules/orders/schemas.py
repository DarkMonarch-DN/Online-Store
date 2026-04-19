from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

from src.modules.orders.models import OrderStatus


class OrderCreateSchema(BaseModel):
    cart_item_id: int = Field(..., ge=1)
    delivery_address: str = Field(..., min_length=2, max_length=100)


class OrderReadSchema(BaseModel):
    id: int
    status: OrderStatus
    total_price: int
    quantity: int
    price_at_moment: int
    delivery_address: str
    created_at: datetime

    user_id: int
    product_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class AdminOrderUpdateSchema(BaseModel):
    status: OrderStatus | None = None
    quantity: int | None = None
    price_at_moment: int | None = None
    delivery_address: str | None = None

class RequestOrderMeta(BaseModel):
    page: int = Field(..., ge=1)        # Текущая страница
    size: int = Field(..., ge=1)        # Кол-во на странице
 
    sort_by: Literal["quantity", "total_price", "created_at"] = "created_at"
    order: Literal["asc", "desc"] = "desc"

    status: OrderStatus | None = None
    min_total_price: int | None = None
    max_total_price: int | None = None