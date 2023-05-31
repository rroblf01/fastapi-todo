from jose import jwt, JWTError
from src.schemes.users import UserInDb_schema
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from src.config.settings import settings
from fastapi.security import OAuth2PasswordBearer
from src.model.user import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer("/login")


def verify_password(plane_password, hashed_password):
    try:
        return pwd_context.verify(plane_password, hashed_password)
    except:
        return False


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)

    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    return user


def create_token(data: dict) -> str:
    token_jwt = jwt.encode(data, key=settings.SECRET_KEY,
                           algorithm=settings.ALGORITHM)

    return token_jwt


def decode_token(token: str):
    try:
        token_decode = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return token_decode
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})


def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = token_decode.get("sub", None)

        if not username:
            raise HTTPException(status_code=401, detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    return user


def get_user_disabled_current(user: UserInDb_schema = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User_schema")

    return user
