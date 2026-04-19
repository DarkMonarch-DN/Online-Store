from typing import Annotated

from fastapi import Depends
import redis.asyncio as redis

from src.core.config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True
)

def get_redis() -> redis.Redis:
    return redis_client


RedisDep = Annotated[redis.Redis, Depends(get_redis)]