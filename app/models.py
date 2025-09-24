
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    role: UserRole = Field(default=UserRole.USER)  
    orders: List["Order"] = Relationship(back_populates="user")
 

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="orders")
    total_price: float
    status: str = "new"  
    created_at: datetime = Field(default_factory=datetime.now)
    phone: str
    address: str
    payment_method: str = "cod"
    items: List["OrderItem"] = Relationship(back_populates="order")

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    material: str
    color: str
    description: str = ""
    image_url: str
    category: str
    available: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    order: Order = Relationship(back_populates="items")

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship()

    product_name: str
    price: float
    quantity: int