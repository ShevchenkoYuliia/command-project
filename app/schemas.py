
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum
from app.models import UserRole
from pydantic import field_validator

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[UserRole] = UserRole.USER

class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int

class OrderCreate(BaseModel):
    total_price: float
    phone: str
    address: str
    payment_method: str = "cod"
    items: List[OrderItemCreate]
    @field_validator("items")
    def items_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("items must not be empty")
        return v

class OrderItem(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    user_id: Optional[int]
    total_price: float
    status: str
    created_at: datetime
    phone: str
    address: str
    items: List[OrderItem]

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: float
    material: str
    color: str
    description: str = ""
    image_url: str
    category: str
    available: bool = True

class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    material: str
    color: str
    description: str
    image_url: str
    category: str
    available: bool
    created_at: datetime

    class Config:
        from_attributes = True
