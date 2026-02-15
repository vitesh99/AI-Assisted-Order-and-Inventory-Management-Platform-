from fastapi import APIRouter, Depends, HTTPException, Request, Header, BackgroundTasks
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.orders.schemas import OrderCreate, OrderResponse
from app.orders import service as order_service
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.ai.service import process_order_ai 

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    background_tasks: BackgroundTasks,
    idempotency_key: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if idempotency_key:
        from app.core import idempotency
        existing_key = await idempotency.get_idempotency_key(db, idempotency_key)
        if existing_key:
            return existing_key.response_body

    try:
        new_order = await order_service.create_order(db, order, user_id=current_user.id)
        
        # Serialize for response
        # Using fastAPI encoder or model dump would be cleaner but let's assume OrderResponse structure
        # We need to return the object, FastAPI handles serialization.
        # BUT for idempotency we need to save the serialized form.
        # This is tricky without intercepting response.
        # For simplicity in this phase, I will construct a dict response to save.
        
        response_data = OrderResponse.model_validate(new_order).model_dump()
        
        if idempotency_key:
            await idempotency.create_idempotency_key(db, idempotency_key, response_data)
        
        # Trigger AI Background Task
        background_tasks.add_task(process_order_ai, new_order.id)
            
        return new_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_id}/ai-summary")
async def get_order_summary(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.ai.models import OrderAIMetadata
    from sqlalchemy import select
    
    result = await db.execute(select(OrderAIMetadata).where(OrderAIMetadata.order_id == order_id))
    ai_meta = result.scalars().first()
    
    if not ai_meta:
        return {"order_id": order_id, "summary": None, "status": "pending_or_failed"}
        
    return {
        "order_id": order_id, 
        "summary": ai_meta.summary_text,
        "notification_draft": ai_meta.notification_draft,
        "generated_at": ai_meta.created_at
    }

@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Users can see their own orders. Admins can see all? 
    # Req says "List orders with pagination".
    # I'll default to seeing own orders for now.
    return await order_service.list_orders(db, skip, limit, user_id=current_user.id)
