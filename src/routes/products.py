from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.schemes.products import Products_schema, ProductsInDb_schema
from src.config.auth import oauth2_scheme, decode_token
from src.model.products import get_products, create_product, remove_product, get_product
router = APIRouter()


@router.get("/")
def read_products(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> list[ProductsInDb_schema]:
    decoded_token = decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user_id = decoded_token.get('id', 0)
    return get_products(db, user_id)


@router.get("/{id}")
def read_product(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> ProductsInDb_schema:
    decoded_token = decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user_id = decoded_token.get('id', 0)
    return get_product(db, id, user_id)


@router.post("/")
def new_product(payload: Products_schema, db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)) -> ProductsInDb_schema:
    decoded_token = decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user_id = decoded_token.get('id', 0)
    return create_product(db, payload, user_id)


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    user_id = decoded_token.get('id', 0)
    remove_product(db, id, user_id)

    return {"message": "Product deleted successfully"}
