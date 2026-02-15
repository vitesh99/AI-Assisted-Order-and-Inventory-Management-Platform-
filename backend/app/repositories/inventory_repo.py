from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models import Product, Supplier
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.supplier import SupplierCreate

class InventoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(select(Product).options(selectinload(Product.supplier)).where(Product.id == product_id))
        return result.scalars().first()

    async def list_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.db.execute(select(Product).options(selectinload(Product.supplier)).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_product(self, product_in: ProductCreate) -> Product:
        db_product = Product(**product_in.model_dump())
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product

    async def update_stock(self, product_id: int, quantity_delta: int) -> Optional[Product]:
        # Using returning to get updated row
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(stock_quantity=Product.stock_quantity + quantity_delta)
            .execution_options(synchronize_session="fetch")
            .returning(Product)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()
    
    # Supplier Methods
    async def create_supplier(self, supplier_in: SupplierCreate) -> Supplier:
        db_supplier = Supplier(**supplier_in.model_dump())
        self.db.add(db_supplier)
        await self.db.commit()
        await self.db.refresh(db_supplier)
        return db_supplier

    async def list_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        result = await self.db.execute(select(Supplier).offset(skip).limit(limit))
        return result.scalars().all()
