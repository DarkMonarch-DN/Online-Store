from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.modules.products.repository import ProductRepo
from src.modules.products.services import ProductService
from src.core.redis_dep import RedisDep


def get_product_repo(session: AsyncSession = Depends(get_async_session)) -> ProductRepo:
    return ProductRepo(session)

ProductRepoDep = Annotated[ProductRepo, Depends(get_product_repo)]

def get_product_service(product_repo: ProductRepoDep, redis: RedisDep) -> ProductService:
    return ProductService(product_repo, redis)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

