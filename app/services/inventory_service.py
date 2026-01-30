from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.inventory import InventoryItem

class InventoryService:
    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 100):
        return db.query(InventoryItem).offset(skip).limit(limit).all()

    @staticmethod
    def create_item(db: Session, item_in) -> InventoryItem:
        item = InventoryItem(**item_in.dict())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_quantity(db: Session, item_id: int, quantity: int) -> InventoryItem:
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item.quantity = quantity
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def reserve_stock(db: Session, item_id: int, quantity: int) -> InventoryItem:
        """
        Decrement stock for an order. 
        In a real production DB (Postgres), we would use `with_for_update()` here.
        For SQLite, the single-file nature largely serializes writes, but explicit checks are still needed.
        """
        # Select item
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Inventory item {item_id} not found")
        
        if item.quantity < quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for item '{item.name}'. Available: {item.quantity}, Requested: {quantity}")
        
        item.quantity -= quantity
        db.add(item)
        # Note: Commit happens in the caller (OrderService) to ensure atomicity of the whole order
        return item

    @staticmethod
    def restore_stock(db: Session, item_id: int, quantity: int):
        """
        Increment stock when an order is cancelled.
        """
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item:
             # Should be rare if data integrity is maintained
             raise HTTPException(status_code=404, detail=f"Inventory item {item_id} not found during restoration")
        
        item.quantity += quantity
        db.add(item)
