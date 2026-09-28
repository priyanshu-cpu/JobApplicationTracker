from fastapi import APIRouter, Depends, HTTPException
from app.models.application import Application
from app.models.user import User
from app.database import get_db
from app.dependencies.auth import get_current_user



router = APIRouter(prefix="/application")



