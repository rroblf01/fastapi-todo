from src.schemes.users import UserInform_schema
from src.model.models import User
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import Union

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db, username: str) -> Union[User, None]:
    user = db.query(User).filter(User.username == username).first()
    return user


def create_user(db, payload: UserInform_schema):
    user = User(**payload.dict())
    user.password = pwd_context.hash(user.password)
    db.add(user)

    try:
        db.commit()
    except:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    db.refresh(user)

    return user


def remove_user(db, id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
