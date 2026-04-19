from typing import Generic, TypeVar, Optional, Literal, Sequence

from pydantic import BaseModel, Field


T = TypeVar("T")


class ResponseWrapper(BaseModel, Generic[T]):
    status: str = "success"
    data: Optional[T] = None
    message: Optional[str] = None

class ResponseMeta(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    
    sort_by: Optional[str] = None
    order: Optional[str] = "desc"

class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    meta: ResponseMeta