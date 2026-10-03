from fastapi import APIRouter, Depends, HTTPException
from app.models.application import Application
from app.models.user import User
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.application import ApplicationOut, ApplicatoinCreateResponse, ApplicationBase
from sqlalchemy.orm import Session



router = APIRouter(prefix="/application")



@router.post("/create", response_model=ApplicatoinCreateResponse, status_code=201)
def create_application(form_data: ApplicationBase, db:Session = Depends(get_db), user: User =Depends(get_current_user)):
    new_application = Application(**form_data.model_dump(), user_id = user.id)

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return{
        "message" : "application created",
        "data" : new_application
    }

@router.get("/get", response_model=list[ApplicationOut])
def get_applications(db:Session =Depends(get_db), user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(Application.user_id == user.id).all()

    return applications