from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError

from src.core.database import get_async_session
from src.modules.users.models import UserModel
from src.modules.users.repository import UserRepo
from src.modules.users.service import UserService
from src.modules.users import utils


def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepo:
    return UserRepo(session)

UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

def get_user_service(user_repo: UserRepoDep) -> UserService:
    return UserService(user_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    user_repo: UserRepo = Depends(get_user_repo)
) -> UserModel:
    try:
        payload = utils.decode_jwt(token)

        user = await user_repo.get(int(payload["sub"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )

        return user
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expire token invalid."
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature token."
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
    
def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not activated."
        )
    return current_user
    
class RoleChecker:
    def __init__(self, allowed_roles: list) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserModel = Depends(get_current_user)) -> UserModel: #! Позже заменить на active_user
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )
        return user


allow_admin = RoleChecker(["admin"])


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
CurrentActiveUserDep = Annotated[UserModel, Depends(get_current_active_user)]
CurrentAdminDep = Annotated[UserModel, Depends(allow_admin)]
