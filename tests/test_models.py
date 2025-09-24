from datetime import datetime
import pytest
from app.models import User, Order, Product, OrderItem, UserRole

def test_user_model_creation():
    user = User(id=1, name="Anna", email="anna@example.com", hashed_password="hash", role=UserRole.ADMIN)
    assert user.name == "Anna"
    assert user.role == UserRole.ADMIN
    assert user.orders == []

def test_order_model_creation_and_defaults():
    order = Order(
        id=10,
        user_id=1,
        total_price=150.0,
        phone="987654321",
        address="Some Address",
        items=[]
    )
    assert order.status == "new"
    assert order.payment_method == "cod"
    assert isinstance(order.created_at, datetime)

def test_product_model_defaults():
    product = Product(
        id=5,
        name="test",
        price=25.0,
        material="gold",
        color="pink",
        image_url="http://img.com/pink.jpg",
        category="toys"
    )
    assert product.available is True
    assert product.description == ""

def test_orderitem_model_creation():
    order_item = OrderItem(
        id=1,
        order_id=10,
        product_id=5,
        product_name="test",
        price=25.0,
        quantity=3
    )
    assert order_item.price == 25.0
    assert order_item.quantity == 3
