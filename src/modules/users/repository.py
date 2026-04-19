from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, asc, desc

from src.core.repository import BaseRepo
from src.modules.users.models import UserModel, UserRole


class UserRepo(BaseRepo[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(session, UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        user = await self.session.execute(
            select(UserModel)
            .where(UserModel.email == email)
        )
        return user.scalar_one_or_none()
    
    async def get_all(
        self, 
        limit: int,
        offset: int,
        sort_by: str,
        order: str,
        role: UserRole | None = None,
        is_active: bool | None = None
    ):
        query = select(
            UserModel,
            func.count().over().label("total_count")
        )

        if role is not None:
            query = query.where(UserModel.role == role)

        if is_active is not None and is_active == True:
            query = query.where(UserModel.is_active == True)

        column = getattr(UserModel, sort_by, None)
        if column:
            order_func = desc if order == "desc" else asc
            query = query.order_by(order_func(column))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        rows = result.all()
        if not rows:
            return [], 0
        
        users = [row[0] for row in rows]
        total = rows[0][1]

        return users, total