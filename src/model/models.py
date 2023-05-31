from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from typing import List

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    password = Column(String)
    product: Mapped[List["Product"]] = relationship()


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
