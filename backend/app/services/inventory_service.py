from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import InventoryRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.supplier import SupplierCreate, SupplierResponse

class InventoryService:
    def __init__(self, db: AsyncSession):
        self.repo = InventoryRepository(db)

    async def create_product(self, product_in: ProductCreate) -> ProductResponse:
        return await self.repo.create_product(product_in)

    async def get_product(self, product_id: int) -> Optional[ProductResponse]:
        return await self.repo.get_product(product_id)

    async def list_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        return await self.repo.list_products(skip, limit)

    async def update_stock(self, product_id: int, quantity_delta: int) -> Optional[ProductResponse]:
        # Validate stock is sufficient? Repo constraint handles negative stock.
        # But for nice error message, we could check here.
        # For simplicity, let DB constraint catch negative stock for now.
        return await self.repo.update_stock(product_id, quantity_delta)
    
    # Supplier
    async def create_supplier(self, supplier_in: SupplierCreate) -> SupplierResponse:
        return await self.repo.create_supplier(supplier_in)

    async def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[SupplierResponse]:
        return await self.repo.list_suppliers(skip, limit)
