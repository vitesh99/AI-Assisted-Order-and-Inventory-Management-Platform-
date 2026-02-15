from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.inventory.schemas import ProductCreate, ProductResponse
from app.inventory import service as inventory_service
from app.core.config import settings
from app.auth.models import User
# Need to implement get_current_user dependency properly potentially in auth module
# For now, I will use a placeholder or implement it here if needed, 
# but best to have it reusable. I will create a dependency helper in auth/dependencies.py
# Wait, I didn't create that file. I will inline it for now or rely on a shared module.
# Let's create `app/auth/dependencies.py` as it is standard.
# BUT respecting "Match Exactly", I will put it in `app/auth/service.py`?
# I'll rely on `app.auth.service.get_current_user` logic but need the dependency wrapper.

from fastapi.security import OAuth2PasswordBearer
from app.auth.service import get_user_by_email
from app.core import security
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    # Using 'is_superuser' as 'admin' role for simplicity or I should add a role field if specified.
    # Requirement says "Roles: user, admin". I added is_superuser.
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_new_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await inventory_service.create_product(db, product)

@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await inventory_service.list_products(db, skip, limit)
