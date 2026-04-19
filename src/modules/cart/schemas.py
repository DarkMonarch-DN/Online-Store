from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.modules.products.schemas import ProductReadSchema


class CartItemCreateScheme(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)

class CartItemUpdateScheme(BaseModel):
    quantity: int

class CartItemReadScheme(BaseModel):
    id: int
    quantity: int
    created_at: datetime
    product: ProductReadSchema

    model_config = ConfigDict(
        from_attributes=True
    )