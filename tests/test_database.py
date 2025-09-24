import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from app.database import (
    create_user, authenticate_user, hash_password,
    create_order, get_user_orders,
    create_product, get_all_products, get_product_by_id,
)
from app.schemas import UserCreate, ProductCreate, OrderCreate, OrderItemCreate
from app.models import UserRole

# In-memory SQLite (тимчасова база для тестів)
TEST_DB_URL = "sqlite://"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="function")
def db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_create_user_and_authenticate(db):
    user_data = UserCreate(name="example", email="example@example.com", password="secret")
    user = create_user(db, user_data)

    assert user.email == "example@example.com"
    assert user.hashed_password == hash_password("secret")

    authenticated = authenticate_user(db, email="example@example.com", password="secret")
    assert authenticated is not None
    assert authenticated.id == user.id

def test_fail_authentication(db):
    user_data = UserCreate(name="Фейк", email="fail@example.com", password="123456")
    create_user(db, user_data)
    assert authenticate_user(db, "fail@example.com", "wrong") is None

def test_create_product_and_get_by_id(db):
    product_data = ProductCreate(
        name="Кулон Місяць",
        price=900.0,
        material="silver",
        color="white",
        description="Місячне сяйво",
        image_url="/img/moon.jpg",
        category="pendants"
    )
    product = create_product(db, product_data)

    assert product.id is not None
    assert product.name == "Кулон Місяць"

    fetched = get_product_by_id(db, product.id)
    assert fetched.name == "Кулон Місяць"

def test_create_order_with_items(db):
    # Створюємо користувача
    user_data = UserCreate(name="Клієнт", email="client@example.com", password="orderpass")
    user = create_user(db, user_data)

    # Створюємо замовлення
    order_data = OrderCreate(
        total_price=1800,
        phone="123456789",
        address="вул. Шопена, 1",
        payment_method="card",
        items=[
            OrderItemCreate(product_id=1, product_name="Сережки", price=600, quantity=2),
            OrderItemCreate(product_id=2, product_name="Каблучка", price=600, quantity=1),
        ]
    )

    order = create_order(db, order_data, current_user_id=user.id)

    assert order.user_id == user.id
    assert len(order.items) == 2
    assert order.total_price == 1800

def test_get_all_products_filtering(db):
    create_product(db, ProductCreate(
        name="Каблучка",
        price=500,
        material="silver",
        color="blue",
        image_url="/img/ring.jpg",
        category="rings"
    ))
    create_product(db, ProductCreate(
        name="Кулон",
        price=750,
        material="gold",
        color="red",
        image_url="/img/pendant.jpg",
        category="pendants"
    ))

    products = get_all_products(db)
    assert len(products) == 2
