from .products import router as products_router
from .sales import router as sales_router
from .revenue import router as revenue_router
from .inventory import router as inventory_router

__all__ = [
    "products_router",
    "sales_router",
    "revenue_router",
    "inventory_router",
]
