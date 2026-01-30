from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import User
from app.schemas import InventoryItemCreate, InventoryItem as InventoryItemSchema, InventoryItemUpdate
from app.services.inventory_service import InventoryService

router = APIRouter()

@router.get("/", response_model=List[InventoryItemSchema])
def read_inventory_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return InventoryService.get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=InventoryItemSchema)
def create_inventory_item(
    item_in: InventoryItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return InventoryService.create_item(db, item_in)

@router.put("/{item_id}", response_model=InventoryItemSchema)
def update_inventory_item(
    item_id: int,
    item_in: InventoryItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return InventoryService.update_quantity(db, item_id, item_in.quantity)
