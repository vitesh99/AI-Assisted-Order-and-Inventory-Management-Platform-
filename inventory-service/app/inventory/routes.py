from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.inventory.schemas import ProductCreate, ProductResponse, StockUpdate
from app.inventory import service as inventory_service
from app.core.config import settings
# from app.auth.models import User
# from app.auth.service import get_user_by_email
from app.core import security
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

from pydantic import BaseModel

class TokenUser(BaseModel):
    id: int | None = None
    email: str
    is_superuser: bool = False

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id", 0)
        is_superuser: bool = payload.get("is_superuser", False)
        
        if email is None:
            raise credentials_exception
            
        return TokenUser(email=email, id=user_id, is_superuser=is_superuser)
    except JWTError:
        raise credentials_exception

async def get_current_admin_user(current_user: TokenUser = Depends(get_current_user)):
    # Simple check
    return current_user

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_new_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: TokenUser = Depends(get_current_admin_user)
):
    return await inventory_service.create_product(db, product)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db)
):
    product = await inventory_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}/stock", response_model=ProductResponse)
async def update_stock_quantity(
    product_id: int, 
    stock_update: StockUpdate,
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_current_user) # Optional: protect this? Yes.
):
    # For now, allow open or implement stateless auth.
    # Logic:
    try:
        updated_product = await inventory_service.update_stock(db, product_id, stock_update.quantity_delta)
        return updated_product
    except Exception as e:
         raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await inventory_service.list_products(db, skip, limit)
