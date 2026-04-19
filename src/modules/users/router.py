from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.users.schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema, AccessTokenSchema
from src.modules.users.dependencies import UserServiceDep, CurrentUserDep


router = APIRouter()

@router.post("/auth/register", 
    summary="Registration", 
    tags=["Auth"], 
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreateSchema, 
    user_service: UserServiceDep, 
):
    return await user_service.create_user(
        user_data=user_data
    )


@router.post("/auth/login", summary="Login", response_model=AccessTokenSchema, tags=["Auth"])
async def login_for_access_token(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await user_service.login(
        email=form_data.username,
        password=form_data.password
    )


@router.get("/users/me", summary="Get my profile", response_model=UserReadSchema, tags=["Users"])
async def get_me(current_user: CurrentUserDep):
    return current_user

@router.patch("/users", summary="Edit user profile", response_model=UserReadSchema, tags=["Users"])
async def update_user(current_user: CurrentUserDep, user_data: UserUpdateSchema, user_service: UserServiceDep):
    return await user_service.update_user(
        current_user,
        user_data
    )
