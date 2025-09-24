import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas import (
    UserCreate, OrderCreate, OrderItemCreate, OrderItem, Order,
    ProductCreate, ProductRead
)
from app.models import UserRole

def test_usercreate_valid_and_default_role():
    user = UserCreate(name="John", email="john@example.com", password="pass123")
    assert user.name == "John"
    assert user.role == UserRole.USER  

def test_orderitemcreate_valid():
    item = OrderItemCreate(product_id=1, product_name="Toy", price=10.5, quantity=3)
    assert item.quantity == 3
    assert item.price == 10.5

def test_ordercreate_valid_with_items():
    items = [OrderItemCreate(product_id=1, product_name="Toy", price=20.0, quantity=2)]
    order = OrderCreate(total_price=40.0, phone="123456789", address="Some St", items=items)
    assert len(order.items) == 1
    assert order.payment_method == "cod"  

def test_ordercreate_invalid_missing_items():
    with pytest.raises(ValidationError):
        OrderCreate(total_price=20.0, phone="123", address="Addr", items=[])

def test_orderitem_from_attributes():
    class Dummy:
        def __init__(self):
            self.id = 1
            self.product_id = 2
            self.product_name = "ring 1"
            self.price = 15.0
            self.quantity = 5

    dummy = Dummy()
    item = OrderItem.model_validate(dummy)
    assert item.id == dummy.id
    assert item.product_name == "ring 1"

def test_order_from_attributes_with_items():
    class DummyItem:
        def __init__(self):
            self.id = 1
            self.product_id = 2
            self.product_name = "ring 1"
            self.price = 15.0
            self.quantity = 5

    class DummyOrder:
        def __init__(self):
            self.id = 10
            self.user_id = 1
            self.total_price = 100.0
            self.status = "new"
            self.created_at = datetime.now()
            self.phone = "12345"
            self.address = "Addr"
            self.items = [DummyItem()]

    dummy_order = DummyOrder()
    order = Order.model_validate(dummy_order)
    assert order.id == dummy_order.id
    assert len(order.items) == 1
    assert order.items[0].product_name == "ring 1"

def test_productcreate_defaults():
    product = ProductCreate(
        name="ring 11",
        price=10.0,
        material="gold",
        color="red",
        image_url="/static/img/image 88.jpg",
        category="toys"
    )
    assert product.description == ""
    assert product.available is True

def test_productread_from_attributes():
    class DummyProduct:
        def __init__(self):
            self.id = 1
            self.name = "test"
            self.price = 10.0
            self.material = "test"
            self.color = "red"
            self.description = "test test"
            self.image_url = "http://img.url"
            self.category = "test"
            self.available = True
            self.created_at = datetime.now()

    dummy = DummyProduct()
    product = ProductRead.model_validate(dummy)
    assert product.name == "test"
    assert product.available is True
