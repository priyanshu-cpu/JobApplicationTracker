from fastapi import APIRouter, Depends, HTTPException
from app.models.application import Application
from app.models.user import User
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.application import (
    ApplicationOut,
    ApplicationCreateResponse,
    ApplicationBase,
    ApplicationOutUpdated,
    ApplicationUpdateResponse,
    ApplicationUpdate
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/application")



@router.post("/create", response_model=ApplicationCreateResponse, status_code=201)
def create_application(
    form_data: ApplicationBase,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_application = Application(**form_data.model_dump(), user_id=user.id)

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {"message": "application created", "data": new_application}



@router.get("/get", response_model=list[ApplicationOut])
def get_applications(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    if not applications:
        raise HTTPException(status_code=201, detail="not found")
    return applications



@router.get("/get/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .filter(Application.user_id == user.id, Application.id == application_id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="not found")

    return application



@router.put("/update/{application_id}", response_model=ApplicationUpdateResponse)
def update_application(
    application_id: int,
    form_data: ApplicationUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .filter(Application.user_id == user.id, Application.id == application_id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="not found")

    application.status = form_data.status
    application.updated_at = form_data.updated_at
    application.notes = form_data.notes

    db.commit()
    db.refresh(application)

    return{
        "message" : "application updated",
        "data" : application
    }



@router.delete("/delete/{application_id}", status_code=201)
def delete_applicaiton(applicaiton_id: int, db:Session =Depends(get_db), user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == applicaiton_id, Application.user_id == user.id).first()

    if not application:
        raise HTTPException(status_code=404, detail="not found")

    db.delete(application)
    db.commit()

    return []