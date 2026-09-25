from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from app.utils.security import verify_token, credentials_exception
from sqlalchemy.orm import Session
from app.models.user import User


def get_current_user(payload: dict = Depends(verify_token), db:Session = Depends(get_db)):
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError, KeyError):
        raise credentials_exception
    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user