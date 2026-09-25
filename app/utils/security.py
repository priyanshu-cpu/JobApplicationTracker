from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from app.settings import settings


pwd_context = PasswordHash.recommended()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token!",
    headers={"WWW-Authenticate": "Bearer"}
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def generate_password_hash(password:str) ->str :
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update{
        "exp" : expire
    }
    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not payload.get("sub"):
            raise credentials_exception
        return payload
    
    except JWTError:
        raise credentials_exception


