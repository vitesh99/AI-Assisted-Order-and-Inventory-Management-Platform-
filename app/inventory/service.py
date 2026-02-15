from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.inventory.models import Product
from app.inventory.schemas import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundException

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()

async def update_stock(db: AsyncSession, product_id: int, quantity_change: int):
    # This function changes stock by quantity_change (positive to add, negative to reduce)
    # It assumes validation happens before or handles the check constraint error
    product = await get_product(db, product_id)
    if not product:
        raise NotFoundException("Product not found")
    
    product.stock_quantity += quantity_change
    if product.stock_quantity < 0:
        # Should be caught by CheckConstraint ideally, but app level check safe
        raise ValueError("Insufficient stock")
    
    await db.commit()
    await db.refresh(product)
    return product

async def list_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()
