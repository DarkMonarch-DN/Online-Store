from typing import Annotated

from fastapi import Depends

from src.modules.admin.users.services import UserService
from src.modules.users import UserRepoDep


def get_user_service(user_repo: UserRepoDep) -> UserService:
    return UserService(user_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]