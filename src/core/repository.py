from typing import TypeVar, Type, Sequence, Generic

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType")

class BaseRepo(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get(self, id: int) -> ModelType | None:
        return await self.session.get(self.model, id)
    
    # async def get_all(self) -> Sequence[ModelType]:
    #     objs = await self.session.execute(
    #         select(self.model)
    #     )
    #     return objs.scalars().all()
    
    async def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, obj: ModelType, **kwargs) -> ModelType:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)

    async def commit(self) -> None:
        await self.session.commit()
    
    async def refresh(self, obj: ModelType) -> None:
        await self.session.refresh(obj)
