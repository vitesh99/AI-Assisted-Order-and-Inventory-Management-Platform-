from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.inventory_service import InventoryService
from app.schemas.product import ProductCreate, ProductResponse, StockUpdate

router = APIRouter()

def get_service(db: AsyncSession = Depends(get_db)) -> InventoryService:
    return InventoryService(db)

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    service: InventoryService = Depends(get_service)
):
    return await service.create_product(product)

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 100, 
    service: InventoryService = Depends(get_service)
):
    return await service.list_products(skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, 
    service: InventoryService = Depends(get_service)
):
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}/stock", response_model=ProductResponse)
async def update_stock(
    product_id: int, 
    stock_update: StockUpdate, 
    service: InventoryService = Depends(get_service)
):
    product = await service.update_stock(product_id, stock_update.quantity_delta)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
