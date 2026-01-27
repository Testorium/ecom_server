from fastapi import APIRouter
from src.routers.config import api_prefix_config

from .deps import ProductServiceDep
from .schemas import (
    Product,
    ProductCreate,
)

router = APIRouter(prefix=api_prefix_config.v1.products, tags=["Products"])


@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    service: ProductServiceDep,
) -> Product:
    """
    Create a new product.

    Parameters
    ----------
    product : ProductCreate
        The product details to create.

    Returns
    -------
    Product
        The newly created product.
    """
    return await service.create(product)


# @product_router.get("/products", response_model=List[Product])
# async def get_all_products(db_pool: SessionDep) -> List[Product]:
#     """
#     Get a list of all products.

#     Parameters
#     ----------
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     List[Product]
#         A list of all products in the inventory.
#     """
#     query = "SELECT id, name, price, quantity, description FROM products"

#     try:
#         async with db_pool.acquire() as conn:
#             results = await conn.fetch(query)
#             return [Product(**dict(result)) for result in results]
#     except Exception as e:
#         logger.error(f"Error fetching products: {e}")
#         raise HTTPException(status_code=500, detail="Failed to retrieve products")


# @product_router.get("/products/{id}", response_model=Product)
# async def get_product_by_id(
#     db_pool: SessionDep,
#     id: int = Path(..., ge=1),
# ) -> Product:
#     """
#     Get a product by its ID.

#     Parameters
#     ----------
#     id : int
#         The ID of the product.
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     Product
#         The product details for the given ID.
#     """
#     query = "SELECT id, name, price, quantity, description FROM products WHERE id = $1"

#     try:
#         async with db_pool.acquire() as conn:
#             result = await conn.fetchrow(query, id)
#             if result:
#                 return Product(**dict(result))
#             else:
#                 logger.warning(f"Product with ID {id} not found")
#                 raise HTTPException(status_code=404, detail="Product not found")
#     except Exception as e:
#         logger.error(f"Error fetching product by ID: {e}")
#         raise HTTPException(
#             status_code=500, detail="Internal server error during product retrieval"
#         )


# @product_router.put("/products/{id}", response_model=Product)
# async def update_product(
#     db_pool: SessionDep,
#     id: int = Path(..., ge=1),
#     product: ProductUpdate = Body(...),
# ) -> Product:
#     """
#     Update a product by its ID.

#     Parameters
#     ----------
#     id : int
#         The ID of the product to update.
#     product : ProductUpdate
#         The fields to update (partial updates allowed).
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     Product
#         The updated product details.
#     """
#     query = """
#     UPDATE products
#     SET name = COALESCE($1, name),
#         price = COALESCE($2, price),
#         quantity = COALESCE($3, quantity),
#         description = COALESCE($4, description)
#     WHERE id = $5
#     RETURNING id, name, price, quantity, description
#     """

#     try:
#         async with db_pool.acquire() as conn:
#             result = await conn.fetchrow(
#                 query,
#                 product.name,
#                 product.price,
#                 product.quantity,
#                 product.description,
#                 id,
#             )
#             if result:
#                 return Product(**dict(result))
#             else:
#                 logger.warning(f"Product with ID {id} not found for update")
#                 raise HTTPException(status_code=404, detail="Product not found")
#     except Exception as e:
#         logger.error(f"Error updating product: {e}")
#         raise HTTPException(
#             status_code=500, detail="Internal server error during product update"
#         )


# @product_router.delete("/products/{id}")
# async def delete_product(
#     db_pool: SessionDep,
#     id: int = Path(..., ge=1),
# ) -> dict:
#     """
#     Delete a product by its ID.

#     Parameters
#     ----------
#     id : int
#         The ID of the product to delete.
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     dict
#         A message indicating the product was deleted.
#     """
#     query = "DELETE FROM products WHERE id = $1 RETURNING id"

#     try:
#         async with db_pool.acquire() as conn:
#             result = await conn.fetchrow(query, id)
#             if result:
#                 return {"message": "Product deleted successfully"}
#             else:
#                 logger.warning(f"Product with ID {id} not found for deletion")
#                 raise HTTPException(status_code=404, detail="Product not found")
#     except Exception as e:
#         logger.error(f"Error deleting product: {e}")
#         raise HTTPException(
#             status_code=500, detail="Internal server error during product deletion"
#         )


# @product_router.patch("/products/{id}/stock", response_model=Product)
# async def update_product_stock(
#     db_pool: SessionDep,
#     id: int = Path(..., ge=1),
#     stock: ProductStockUpdate = Body(...),
# ) -> Product:
#     """
#     Update the stock (quantity) of a product by its ID.

#     Parameters
#     ----------
#     id : int
#         The ID of the product to update.
#     stock : ProductStockUpdate
#         The new quantity for the product.
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     Product
#         The updated product with new stock quantity.
#     """
#     query = """
#     UPDATE products
#     SET quantity = $1
#     WHERE id = $2
#     RETURNING id, name, price, quantity, description
#     """
#     try:
#         async with db_pool.acquire() as conn:
#             result = await conn.fetchrow(query, stock.quantity, id)
#             if result:
#                 return Product(**dict(result))
#             else:
#                 raise HTTPException(status_code=404, detail="Product not found")
#     except Exception as e:
#         logger.error(f"Error updating product stock: {e}")
#         raise HTTPException(
#             status_code=500, detail="Internal server error during product stock update"
#         )


# @product_router.get("/products/filter/price", response_model=List[Product])
# async def filter_products_by_price(
#     db_pool: SessionDep,
#     min_price: float = Query(...),
#     max_price: float = Query(...),
# ) -> List[Product]:
#     """
#     Get products within a specific price range.

#     Parameters
#     ----------
#     min_price : float
#         The minimum price for filtering.
#     max_price : float
#         The maximum price for filtering.
#     db_pool : asyncpg.Pool, optional
#         Database connection pool injected by dependency.

#     Returns
#     -------
#     List[Product]
#         A list of products within the specified price range.
#     """
#     query = """
#     SELECT id, name, price, quantity, description
#     FROM products
#     WHERE price BETWEEN $1 AND $2
#     """
#     try:
#         async with db_pool.acquire() as conn:
#             results = await conn.fetch(query, min_price, max_price)
#             return [Product(**dict(result)) for result in results]
#     except Exception as e:
#         logger.error(f"Error filtering products by price: {e}")
#         raise HTTPException(
#             status_code=500, detail="Internal server error during price filtering"
#         )
