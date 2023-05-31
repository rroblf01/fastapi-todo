from pydantic import BaseModel

class Products_schema(BaseModel):
    name: str
    description: str
    price: float

class ProductsInDb_schema(Products_schema):
    id: int
    user_id: int

    class Config:
        orm_mode = True
