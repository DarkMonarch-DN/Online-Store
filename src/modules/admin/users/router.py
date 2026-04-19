from fastapi import APIRouter, Query

from src.core.schemas import ResponseWrapper, ResponseMeta, PaginatedResponse
from src.modules.users import CurrentAdminDep
from src.modules.users.schemas import UserReadSchema, RequestUserMeta, AdminUpdateUserSchema
from src.modules.admin.users.dependencies import UserServiceDep

router = APIRouter()


@router.get("/", summary="Get all users", response_model=ResponseWrapper[PaginatedResponse[UserReadSchema]])
async def get_all_users(
    current_user: CurrentAdminDep,
    user_service: UserServiceDep,
    params: RequestUserMeta = Query()
):
    users, total = await user_service.get_all(params)
    return ResponseWrapper(
        data=PaginatedResponse(
            items=users,
            meta=ResponseMeta(
                total=total,
                page=params.page,
                size=params.size,
                pages=total // params.size,
                sort_by=params.sort_by,
                order=params.order
            )
        ),
        message="Users get success"
    )

@router.get("/{user_id}", summary="Get user by id", response_model=ResponseWrapper[UserReadSchema])
async def get_user_by_id(
    user_id: int,
    current_user: CurrentAdminDep,
    user_service: UserServiceDep
):
    user = await user_service.get_one(user_id)
    return ResponseWrapper(
        data=user,
        message="User get success"
    )

@router.patch("/{user_id}", summary="Update user by id", response_model=ResponseWrapper[UserReadSchema])
async def update_user_by_id(
    user_id: int,
    user_data: AdminUpdateUserSchema,
    current_user: CurrentAdminDep,
    user_service: UserServiceDep
):
    user = await user_service.update_user(user_id, user_data)
    return ResponseWrapper(
        data=user,
        message="Success updated user"
    )

@router.delete("/{user_id}", summary="Delete user", response_model=ResponseWrapper)
async def delete_user(
    user_id: int,
    current_user: CurrentAdminDep,
    user_service: UserServiceDep
):
    await user_service.delete_user(user_id)
    return ResponseWrapper(
        message="User success deleted"
    )