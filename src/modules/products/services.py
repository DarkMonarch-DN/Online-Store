import json
import hashlib

from fastapi import HTTPException, status
from redis.asyncio import Redis

from src.modules.products.repository import ProductRepo
from src.modules.users.models import UserModel
from src.modules.products.schemas import (
    ProductCreateSchema, 
    ProductUpdateSchema,
    RequestProductMeta, 
    ProductReadSchema
)


class ProductService:
    def __init__(self, product_repo: ProductRepo, redis: Redis) -> None:
        self.product_repo = product_repo
        self.redis = redis

    async def get_all(self, params: RequestProductMeta):
        params_dict = params.model_dump(exclude_none=True)
        params_str = json.dumps(params_dict, sort_keys=True)
        cache_key = f"products:{hashlib.md5(params_str.encode()).hexdigest()}"

        cached_data = await self.redis.get(cache_key)
        if cached_data:
            data = json.loads(cached_data)
            return data["products"], data["total"]
            

        limit = params.size
        offset = (params.page - 1) * limit

        products, total = await self.product_repo.get_all(
            limit=limit,
            offset=offset,
            **params.model_dump(exclude={"page", "size"})
        )

        result_to_cache = {
            "products": [ProductReadSchema.model_validate(p).model_dump(mode="json") for p in products],
            "total": total
        }

        await self.redis.set(
            name=cache_key,
            value=json.dumps(result_to_cache),
            ex=300
        )

        return products, total
    
    async def get_one(self, product_id: int):
        product = await self.product_repo.get(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    
    async def create(self, current_user: UserModel, product_data: ProductCreateSchema):
        product = await self.product_repo.create(
            **product_data.model_dump(),
            user_id=current_user.id
        )
        await self.product_repo.commit()
        await self.clear_product_cache()
        return product
    
    async def update(self, product_id: int, product_data: ProductUpdateSchema):
        product = await self.get_one(product_id)
        new_product = await self.product_repo.update(
            product,
            **product_data.model_dump(exclude_unset=True)
        )
        await self.clear_product_cache()
        return new_product
    
    async def delete(self, product_id: int) -> None:
        product = await self.get_one(product_id)
        await self.product_repo.delete(product)
        await self.product_repo.commit()
        await self.clear_product_cache()   

    async def clear_product_cache(self):
        # Ищем все ключи, начинающиеся с products:
        keys = await self.redis.keys("products:*")
        if keys:
            await self.redis.delete(*keys)