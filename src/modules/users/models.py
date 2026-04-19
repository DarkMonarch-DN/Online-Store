from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

from src.core.database import Base

if TYPE_CHECKING:
    from src.modules.products.models import ProductModel
    from src.modules.cart.models import CartModel
    from src.modules.orders.models import OrderModel

class UserRole(str, Enum):
    """User roles enum"""
    admin = "admin"
    regular = "regular"


class UserModel(Base):
    """User model
    ```
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=False)

    role: Mapped[UserRole] = mapped_column(default=UserRole.regular)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    cart_items: Mapped[list["CartModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    ```
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=False)

    role: Mapped[UserRole] = mapped_column(default=UserRole.regular)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    cart_items: Mapped[list["CartModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )