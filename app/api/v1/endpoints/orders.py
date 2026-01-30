from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models import Order, OrderItem, InventoryItem, User
from app.schemas import OrderCreate, Order as OrderSchema

router = APIRouter()

@router.get("/", response_model=List[OrderSchema])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()

@router.post("/", response_model=OrderSchema)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # 1. Calculate total and verify inventory
    total_amount = 0.0
    items_to_create = []

    # Use a transaction-like approach or just simple checks
    # For production, we'd want row locking (SELECT FOR UPDATE)
    
    for item_in in order_in.items:
        inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_in.inventory_item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail=f"Inventory item {item_in.inventory_item_id} not found")
        
        if inventory_item.quantity < item_in.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for item {inventory_item.name}")
        
        # Deduct stock
        inventory_item.quantity -= item_in.quantity
        
        # Add to list
        # Note: In a real app we'd fetch price from inventory_item, here we assume 0 or handle price management differently
        # For this phase 1, we haven't added price to inventory, let's assume a dummy logic or 0
        price = 0.0 
        total_amount += price * item_in.quantity
        
        items_to_create.append({
            "inventory_item_id": item_in.inventory_item_id,
            "quantity": item_in.quantity,
            "price_at_purchase": price,
            "inventory_item": inventory_item # keep reference to commit changes
        })

    # 2. Create Order
    db_order = Order(
        user_id=current_user.id,
        status="completed", # Immediately completed for simplicity in Phase 1
        total_amount=total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 3. Create OrderItems
    for item_data in items_to_create:
        db_item = OrderItem(
            order_id=db_order.id,
            inventory_item_id=item_data["inventory_item_id"],
            quantity=item_data["quantity"],
            price_at_purchase=item_data["price_at_purchase"]
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order
