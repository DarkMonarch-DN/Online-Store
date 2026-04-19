from fastapi import APIRouter, status

from src.modules.users import CurrentAdminDep
from src.core.schemas import ResponseWrapper
from src.modules.products.schemas import ProductCreateSchema, ProductUpdateSchema, ProductReadSchema
from src.modules.products import ProductServiceDep

router = APIRouter()

@router.post("/", 
    summary="Create product", 
    response_model=ResponseWrapper[ProductReadSchema],
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_data: ProductCreateSchema,
    current_user: CurrentAdminDep,
    product_service: ProductServiceDep
):
    product = await product_service.create(
        current_user,
        product_data
    )
    return ResponseWrapper(
        data=product,
        message="Success created product"
    )

@router.patch("/{product_id}", summary="Update product", response_model=ResponseWrapper[ProductReadSchema])
async def update_product(
    product_id: int,
    current_user: CurrentAdminDep,
    product_service: ProductServiceDep,
    product_data: ProductUpdateSchema,
):
    product = await product_service.update(
        product_id,
        product_data
    )
    return ResponseWrapper(
        data=product,
        message="Success updated product"
    )

@router.delete("/{product_id}", summary="Delete product", response_model=ResponseWrapper)
async def delete_product(
    product_id: int,
    current_user: CurrentAdminDep,
    product_service: ProductServiceDep
):
    await product_service.delete(
        product_id
    )
    return ResponseWrapper(
        message="Success deleted product"
    )
