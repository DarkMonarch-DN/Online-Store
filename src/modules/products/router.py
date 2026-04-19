from fastapi import APIRouter, Query
from src.core.schemas import ResponseMeta, ResponseWrapper, PaginatedResponse
from src.modules.products.schemas import ProductReadSchema, RequestProductMeta
from src.modules.products.dependencies import ProductServiceDep


router = APIRouter()

@router.get("/", summary="Get all products", 
    response_model=ResponseWrapper[
        PaginatedResponse[
            ProductReadSchema
        ]
    ]
)
async def get_all_products(
    product_service: ProductServiceDep,
    params: RequestProductMeta = Query()
):
    products, total = await product_service.get_all(params)
    return ResponseWrapper(
        data=PaginatedResponse(
            items=products,
            meta=ResponseMeta(
                total=total,
                page=params.page,
                size=params.size,
                pages=total // params.size,
                sort_by=params.sort_by,
                order=params.order
            )
        )
    )


@router.get("/{product_id}", summary="Get product", response_model=ProductReadSchema)
async def get_product(
    product_id: int, 
    product_service: ProductServiceDep,
):
    return await product_service.get_one(product_id)