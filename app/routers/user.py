from fastapi import APIRouter
from app.schemas.user import User, UserOut
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth")

router.post("register")
async def create_user(form_data: User, db:Session = Depends(get_db)):
    pass