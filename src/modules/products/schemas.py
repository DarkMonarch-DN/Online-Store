from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.core.config import settings


def validate_category_list(value: list[str]) -> list[str]:
    if value is None: return None
    result = []
    for cat in value:
        if cat in settings.CATEGORIES:
            result.append(cat.lower())
        else:
            raise ValueError(f"Invalid category: {cat}, Allowed categories: {settings.CATEGORIES}")
    return result


class ProductBaseSchema(BaseModel):
    """Product base schema"""
    title: str = Field(..., min_length=2, max_length=50, description="Название товара")
    price: int = Field(..., ge=0, description="Цена товара")
    stock_quantity: int = Field(..., ge=0, description="Количество товара")
    description: str = Field(..., min_length=50, max_length=5000, description="Описание товара")

class ProductReadSchema(ProductBaseSchema):
    """Product read schema"""
    id: int
    created_at: datetime
    categories: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductCreateSchema(ProductBaseSchema):
    """Product create schema"""
    categories: list[str]
    
    _validate_cats = field_validator("categories")(validate_category_list)

class ProductUpdateSchema(BaseModel):
    """Product update schema"""
    title: Optional[str] = Field(None, min_length=2, max_length=50, description="Название товара")
    price: Optional[int] = Field(None, ge=0, description="Цена товара")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Количество товара")
    description: Optional[str] = Field(None, min_length=50, max_length=5000, description="Описание товара")

    categories: Optional[list[str]] = None

    _validate_cats = field_validator("categories")(validate_category_list)


class RequestProductMeta(BaseModel): 
    page: int = Field(..., ge=1)        # Текущая страница
    size: int = Field(..., ge=1)        # Кол-во на странице

    sort_by: Literal["title", "price", "created_at"] = "created_at"
    order: Literal["asc", "desc"] = "desc"

    min_price: float | None = None
    max_price: float | None = None
    categories: list[str] | None = None
    search: str | None = None

    _validate_cats = field_validator("categories")(validate_category_list)