from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.AUTH_SERVICE_URL}/api/v1/auth/login")

class TokenUser(BaseModel):
    id: int
    email: str
    is_superuser: bool = False

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        is_superuser: bool = payload.get("is_superuser", False)
        
        if email is None or user_id is None:
            raise credentials_exception
            
        return TokenUser(id=user_id, email=email, is_superuser=is_superuser)
    except JWTError:
        raise credentials_exception

async def get_current_admin_user(current_user: TokenUser = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
