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
            item_details = ", ".join([f"{item.quantity}x Product_ID:{item.product_id}" for item in order.items])
            
            prompt = (
                f"You are an order management assistant. "
                f"Generate a short, professional order summary for: "
                f"Order ID {order.id}, Status {order.status}, Total {order.total_amount}. "
                f"Items: {item_details}. "
                f"Make it human readable."
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
