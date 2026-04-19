from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey

from src.core.database import Base
if TYPE_CHECKING:
    from src.modules.products.models import ProductModel
    from src.modules.users.models import UserModel


class CartModel(Base):
    """Cart item model"""
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="cart_items")
    
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    product: Mapped["ProductModel"] = relationship(back_populates="in_carts")

