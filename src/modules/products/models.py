from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, ARRAY, String

from src.core.database import Base

if TYPE_CHECKING:
    from src.modules.users.models import UserModel
    from src.modules.cart.models import CartModel
    from src.modules.orders.models import OrderModel

class ProductModel(Base):
    """Product model"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[int]
    # Количество товара
    stock_quantity: Mapped[int]
    description: Mapped[str]
    categories: Mapped[list[str]] = mapped_column(ARRAY(String))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="products")

    in_carts: Mapped[list["CartModel"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )
    in_orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )