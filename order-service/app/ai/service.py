from app.db.session import AsyncSessionLocal
from app.ai.client import ai_client
from app.ai.models import OrderAIMetadata
from app.orders.models import Order
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging
import asyncio

logger = logging.getLogger(__name__)

async def process_order_ai(order_id: int):
    """
    Background task to generate AI summary for an order.
    Creates its own DB session.
    """
    if not ai_client.enabled:
        return

    logger.info(f"Starting AI processing for Order {order_id}")
    
    async with AsyncSessionLocal() as db:
        try:
            # Fetch Order with Items to give context to AI
            result = await db.execute(
                select(Order)
                .options(selectinload(Order.items))
                .where(Order.id == order_id)
            )
            order = result.scalars().first()
            
            if not order:
                logger.warning(f"Order {order_id} not found during AI processing")
                return

            # Construct Prompt
            # In a real app, we'd fetch product names too, but IDs are fine for this demo
            # Fetch product names for better AI context
            item_details_list = []
            for item in order.items:
                try:
                     # We use inventory_client. Since this is async, we can do it.
                     # Note: ai/service.py needs to import inventory_client
                     # To avoid circular imports if any, verify. 
                     # service.py imports from app.db, app.ai, app.orders. 
                     # inventory_client is in app.core.
                     from app.core.service_clients import inventory_client
                     product = await inventory_client.get_product(item.product_id)
                     name = product.name if product else f"Product_{item.product_id}"
                     item_details_list.append(f"{item.quantity}x {name}")
                except Exception:
                     item_details_list.append(f"{item.quantity}x Product_ID:{item.product_id}")
            
            item_details = ", ".join(item_details_list)
            
            prompt = (
                f"You are an order management assistant. "
                f"Generate a short, professional order summary for: "
                f"Order ID {order.id}, Status {order.status}, Total ₹{order.total_amount}. "
                f"Items: {item_details}. "
                f"Make it human readable. Use the Indian Rupee symbol (₹) for all currency values."
            )

            # Call AI for Summary
            summary = await ai_client.generate_text(prompt)
            
            # Call AI for Notification Draft
            notification_prompt = (
                f"Write a short, polite email notification to the customer for Order #{order.id} "
                f"which has been {order.status}. Total: {order.total_amount}. "
                f"Do not include subject line, just the body."
            )
            notification = await ai_client.generate_text(notification_prompt)
            
            if summary or notification:
                # Store Result
                ai_meta = OrderAIMetadata(
                    order_id=order.id,
                    summary_text=summary,
                    notification_draft=notification
                )
                db.add(ai_meta)
                await db.commit()
                logger.info(f"AI Summary & Notification saved for Order {order_id}")
            else:
                logger.warning(f"AI returned no content for Order {order_id}")

        except Exception as e:
            logger.error(f"Error in process_order_ai: {e}")
            # No re-raise, this is a background task
