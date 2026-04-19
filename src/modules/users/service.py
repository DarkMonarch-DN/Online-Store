from fastapi import HTTPException, status

from src.modules.users import schemas
from src.modules.users.repository import UserRepo
from src.modules.users import utils
from src.modules.users.models import UserModel
from src.modules.users.schemas import UserUpdateSchema

class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def create_user(self, user_data: schemas.UserCreateSchema):
        existing = await self.user_repo.get_by_email(user_data.email)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user has already been registered."
            )

        user = await self.user_repo.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=utils.hash_password(user_data.password)
        )
        
        await self.user_repo.commit()

        return {
            "success": True,
            "message": "Registration was successful.",
            "username": user.username
        }
    
    async def login(self, email: str, password: str):
        unauth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

        user = await self.user_repo.get_by_email(email)

        if not user:
            raise unauth_exception
        if not utils.check_password(password, user.hashed_password):
            raise unauth_exception
        
        access_token = utils.encode_jwt(
            {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role
            }
        )
        return schemas.AccessTokenSchema(
            access_token=access_token,
            token_type="bearer"
        )
    
    async def update_user(self, current_user: UserModel, user_data: UserUpdateSchema) -> UserModel:
        return await self.user_repo.update(
            current_user,
            **user_data.model_dump(exclude_unset=True)
        )