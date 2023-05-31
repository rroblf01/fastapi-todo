from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.model.user import get_user, create_user, remove_user
from src.schemes.users import UserInform_schema, UserInDb_schema
from passlib.context import CryptContext
from src.config.auth import oauth2_scheme, decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.get("/")
def read_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserInDb_schema:
    decoded_token = decode_token(token)

    return get_user(db, decoded_token.get('sub', 0))


@router.post("/")
def new_user(payload: UserInform_schema, db: Session = Depends(get_db)) -> UserInDb_schema:
    return create_user(db, payload)


@router.delete("/")
def delete_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)

    user_id = decoded_token.get('id', -1)
    remove_user(db, user_id)

    return {"message": "User deleted successfully"}
