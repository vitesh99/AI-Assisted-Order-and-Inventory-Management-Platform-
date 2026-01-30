from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import InventoryItem, User
from app.schemas import InventoryItemCreate, InventoryItem as InventoryItemSchema, InventoryItemUpdate

router = APIRouter()

@router.get("/", response_model=List[InventoryItemSchema])
def read_inventory_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return db.query(InventoryItem).offset(skip).limit(limit).all()

@router.post("/", response_model=InventoryItemSchema)
def create_inventory_item(
    item_in: InventoryItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    item = InventoryItem(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{item_id}", response_model=InventoryItemSchema)
def update_inventory_item(
    item_id: int,
    item_in: InventoryItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.quantity = item_in.quantity
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
