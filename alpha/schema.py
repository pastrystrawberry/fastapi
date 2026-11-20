from pydantic import BaseModel,EmailStr, Field, ConfigDict
from typing import Literal
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str=Field(min_length=8)
class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    model_config=ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class ProductCreate(BaseModel):
    name:str
    price:float
class PurchaseCreate(BaseModel):
    product_id:int
    quantity: int
class Token(BaseModel):
    access_token: str
    token_type: str
class ProductReactionCreate(BaseModel):
    reaction: Literal["like", "dislike"]