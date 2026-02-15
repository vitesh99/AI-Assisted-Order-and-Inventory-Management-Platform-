from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.orders.models import Order, OrderItem, OrderStatus
from app.orders.schemas import OrderCreate
from app.inventory.service import get_product, update_stock
from app.utils.exceptions import NotFoundException, StockException

async def create_order(db: AsyncSession, order_data: OrderCreate, user_id: int):
    # Initialize order
    new_order = Order(user_id=user_id, status=OrderStatus.CREATED.value, total_amount=0.0)
    db.add(new_order)
    await db.flush() # get ID

    total_amount = 0.0
    
    for item in order_data.items:
        product = await get_product(db, item.product_id)
        if not product:
            raise NotFoundException(f"Product {item.product_id} not found")
        
        # Check stock (simple check, better with locking or versioning for high concurrency)
        if product.stock_quantity < item.quantity:
            raise StockException(f"Insufficient stock for product {product.name}")
        
        # Deduct stock
        await update_stock(db, item.product_id, -item.quantity)
        
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)
        total_amount += product.price * item.quantity
    
    new_order.total_amount = total_amount
    new_order.status = OrderStatus.CONFIRMED.value # Automatically confirm if stock valid per reqs? 
    # Req says "Create order (validate inventory)". "Order status lifecycle (CREATED -> CONFIRMED -> CANCELLED)".
    # Usually creation is CREATED, then payment/confirm moves to CONFIRMED.
    # But for "Core Backend", let's assume immediate confirmation if stock is available as there is no payment gateway.
    # Or I can leave it as CREATED and add a confirm endpoint.
    # "Create order (validate inventory)" implies validation happens at creation.
    # I will set it to CONFIRMED for simplicity since stock is deducted. 
    # If I don't set to CONFIRMED, I shouldn't deduct stock yet? Or hold it?
    # Simple approach: Deduct stock -> CONFIRMED.
    
    await db.commit()
    await db.refresh(new_order)
    # Eager load items for response
    # We need to re-fetch with items
    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == new_order.id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def list_orders(db: AsyncSession, skip: int = 0, limit: int = 10, user_id: int = None):
    stmt = select(Order).options(selectinload(Order.items)).offset(skip).limit(limit)
    if user_id:
        stmt = stmt.where(Order.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()
