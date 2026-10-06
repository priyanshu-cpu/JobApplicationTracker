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
    ApplicationUpdate,
    ApplicationPatch,
)
from sqlalchemy.orm import Session
from sqlalchemy import func

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

    db.commit()
    db.refresh(application)

    return {"message": "application updated", "data": application}


@router.delete("/delete/{application_id}", status_code=204)
def delete_applicaiton(
    application_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user.id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="not found")

    db.delete(application)
    db.commit()

    return


@router.patch("/update/{application_id}", response_model=ApplicationUpdateResponse)
def patch_application(
    application_id: int,
    form_data: ApplicationPatch,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="not found")

    changes = form_data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="no fields to update")

    for field, value in changes.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return {"message": "application updated", "data": application}


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total = (
        db.query(func.count(Application.id))
        .filter(Application.user_id == user.id)
        .scalar()
    )

    rows = (
        db.query(Application.status, func.count(Application.id))
        .filter(Application.user_id == user.id)
        .group_by(Application.status)
        .all()
    )

    by_status = {status: count for status, count in rows}

    return{
        "total" : total,
        "by_status" : by_status
    }