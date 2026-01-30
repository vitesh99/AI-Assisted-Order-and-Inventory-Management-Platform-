from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate
from app.services.inventory_service import InventoryService

class OrderService:
    @staticmethod
    def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_order(db: Session, user_id: int, order_in: OrderCreate) -> Order:
        # Start transaction explicitly if needed, but Session handles it
        total_amount = 0.0
        items_to_create = []

        try:
            for item_in in order_in.items:
                # 1. Reserve Stock (Validates existence and quantity)
                inventory_item = InventoryService.reserve_stock(db, item_in.inventory_item_id, item_in.quantity)
                
                # 2. Calculate Price (Mock price for now as discussed)
                price = 10.0 # Placeholder: In real app, fetch from inventory_item.price
                total_amount += price * item_in.quantity

                items_to_create.append({
                    "inventory_item_id": item_in.inventory_item_id,
                    "quantity": item_in.quantity,
                    "price_at_purchase": price
                })

            # 3. Create Order
            db_order = Order(
                user_id=user_id,
                status=OrderStatus.PENDING,
                total_amount=total_amount
            )
            db.add(db_order)
            db.flush() # Flush to get ID

            # 4. Create Order Items
            for item_data in items_to_create:
                db_item = OrderItem(
                    order_id=db_order.id,
                    inventory_item_id=item_data["inventory_item_id"],
                    quantity=item_data["quantity"],
                    price_at_purchase=item_data["price_at_purchase"]
                )
                db.add(db_item)
            
            # 5. Confirm Order (If payment was integrated, we might wait here)
            db_order.status = OrderStatus.CONFIRMED
            db.commit()
            db.refresh(db_order)
            return db_order

        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def cancel_order(db: Session, order_id: int, user_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Order is already cancelled")
        
        # Restore stock
        try:
            for item in order.items:
                InventoryService.restore_stock(db, item.inventory_item_id, item.quantity)
            
            order.status = OrderStatus.CANCELLED
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e
