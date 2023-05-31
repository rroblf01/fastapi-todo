from src.model.models import User
from fastapi import HTTPException
from src.model.models import Product
from src.schemes.products import Products_schema
from typing import Union


def get_products(db, user_id: int) -> Union[User, None]:
    return db.query(Product).filter(Product.user_id == user_id).all()


def get_product(db, id: int, user_id: int) -> Union[User, None]:
    product = db.query(Product).filter(
        Product.id == id, Product.user_id == user_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


def create_product(db, payload: Products_schema, user_id) -> Union[User, None]:
    product = Product(**payload.dict())
    product.user_id = user_id

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def remove_product(db, id: int, user_id: int):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this product")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
