from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.db.session import get_db
from app.auth.schemas import UserCreate, UserResponse, Token
from app.auth import service as auth_service
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await auth_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await auth_service.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Login attempt for user: '{form_data.username}'")
    logger.info(f"Password length: {len(form_data.password)}")
    logger.info(f"Password first char: {form_data.password[0] if form_data.password else 'EMPTY'}")
    
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email, 
        expires_delta=access_token_expires,
        claims={"id": user.id, "is_superuser": user.is_superuser}
    )
    return {"access_token": access_token, "token_type": "bearer"}
