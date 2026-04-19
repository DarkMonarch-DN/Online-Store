from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func

from src.core.database import Base
if TYPE_CHECKING:
    from src.modules.users.models import UserModel
    from src.modules.products.models import ProductModel


class OrderStatus(str, Enum):
    """Order status enum"""
    PENDING = "pending"      # ожидает подтверждения
    CONFIRMED = "confirmed"  # подтвержден (можно дальше обрабатывать)
    CANCELLED = "cancelled"

class OrderModel(Base):
    """Order model"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.CONFIRMED)
    total_price: Mapped[int]
    quantity: Mapped[int]
    price_at_moment: Mapped[int]
    delivery_address: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="orders")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    product: Mapped["ProductModel"] = relationship(back_populates="in_orders")
