from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.order_service import OrderService
from app.services.ai_service import AIService
from app.schemas.order import OrderCreate, OrderResponse, OrderStatus
from app.schemas.ai import ChatResponse
from app.core import security
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(db)

def get_ai_service() -> AIService:
    return AIService()

async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    # Minimal auth check to get ID
    try:
        payload = security.jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("id")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_service)
    # background_tasks: BackgroundTasks # For AI? Yes later.
):
    return await service.create_order(user_id, order)

@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    skip: int = 0, 
    limit: int = 100, 
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_service)
):
    return await service.list_orders(user_id, skip, limit)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_service)
):
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != user_id:
         raise HTTPException(status_code=403, detail="Not authorized")
    return order

@router.get("/{order_id}/ai-summary", response_model=dict)
async def get_ai_summary(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    service: OrderService = Depends(get_service),
    ai_service: AIService = Depends(get_ai_service)
):
    order = await service.get_order(order_id)
    if not order:
         raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != user_id:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    # Check if summary exists (Logic should be in Service, but simple enough here for now)
    # Ideally: order_service.get_summary(order_id)
    # For speed: Ask AI directly
    
    prompt = f"Analyze this order: ID {order.id}, Total ₹{order.total_amount}, Items: {len(order.items)}. Status: {order.status}. Provide a brief business summary."
    response = await ai_service.chat(prompt, context="order_summary")
    
    return {"summary": response.response}
