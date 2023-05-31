from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.config.auth import authenticate_user, create_token
from src.config.db import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_jwt = create_token({"sub": user.username, "id": user.id})
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }
