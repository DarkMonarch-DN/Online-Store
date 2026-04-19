from fastapi import HTTPException, status

from src.modules.users.repository import UserRepo
from src.modules.users.schemas import AdminUpdateUserSchema, RequestUserMeta


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get_all(self, params: RequestUserMeta):
        limit: int = params.size
        offset: int = (params.page - 1) * limit

        users, total = await self.user_repo.get_all(
            limit=limit,
            offset=offset,
            sort_by=params.sort_by,
            order=params.order,
            role=params.role,
            is_active=params.is_active
        )

        return users, total

    async def get_one(self, user_id: int):
        user = await self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user
    
    async def update_user(self, user_id: int, user_data: AdminUpdateUserSchema):
        user = await self.get_one(user_id)
        new_user = await self.user_repo.update(
            user,
            **user_data.model_dump(exclude_unset=True)
        )
        return new_user
    
    async def delete_user(self, user_id) -> None:
        user = await self.get_one(user_id)
        await self.user_repo.delete(user)
        await self.user_repo.commit()