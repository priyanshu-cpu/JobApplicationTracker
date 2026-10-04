from fastapi import APIRouter, HTTPException, status
from app.schemas.user import User, UserCreateResponse, UserOut
from app.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.models.application import Application
from app.utils.security import generate_password_hash, verify_password, create_token
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserCreateResponse)
def create_user(form_data: User, db: Session = Depends(get_db)):
    username = (
        db.query(UserModel).filter(UserModel.username == form_data.username).first()
    )
    if username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    if form_data.email is not None:
        email = db.query(UserModel).filter(UserModel.email == form_data.email).first()
        if email is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    password_hash = generate_password_hash(form_data.password)

    user = UserModel(
        username=form_data.username,
        email=form_data.email,
        hashed_password=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "user created successfully!", "user": user}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub" : str(user.id)
    })
    return{
        "access_token" : token,
        "token_type" : "bearer"
    }



@router.get("/me", response_model=UserOut)
def me(user:User = Depends(get_current_user)):
    return user


@router.delete("/me", status_code=204)
def delete_me(
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),):
    
    db.delete(user)
    db.commit()
    return