
from sqlalchemy import (
    Column, Integer, String, Numeric,
    ForeignKey, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from .database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_Hash = Column(String(255), nullable=True)
    purchases = relationship("Purchase", back_populates="user")
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    purchases = relationship("Purchase", back_populates="product")
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchased_at = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="purchases")
class ProductReaction(Base):
    __tablename__= "product_reactions"
    id= Column(Integer,primary_key=True,index=True)
    user_id =Column(Integer,ForeignKey("users.id"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    reaction=Column(String(10),nullable=False)
    __table_args__=(
        UniqueConstraint("user_id","product_id"),
    )