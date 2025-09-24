from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel
from fastapi import Depends, Request, Cookie
from typing import Generator
from app.models import User, Order, OrderItem, Product
from app.models import UserRole
from app.schemas import UserCreate, OrderCreate, ProductCreate
import hashlib
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
def create_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        seed_products(db)
        seed_admin(db)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_current_user(
    request: Request,
    user_id: str = Cookie(None), 
    db: Session = Depends(get_db)
):
    if user_id is None:
        return None 
    
    try:
        user_id_int = int(user_id)
        user = db.query(User).filter(User.id == user_id_int).first()
        if not user:
            return None
        return user
    except ValueError:
        return None

def create_user(db: Session, user_data: UserCreate):
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role if hasattr(user_data, 'role') else UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_order(db: Session, order_data: OrderCreate, current_user_id: int = None):
    order = Order(
        user_id=current_user_id,
        total_price=order_data.total_price,
        phone=order_data.phone,
        address=order_data.address,
        payment_method=order_data.payment_method,  
        status="new"
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            product_name=item_data.product_name,
            price=item_data.price,
            quantity=item_data.quantity
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    return order

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def create_product(db: Session, product_data: ProductCreate):
    product = Product(
        name=product_data.name,
        price=product_data.price,
        material=product_data.material,
        color=product_data.color,
        description=product_data.description,
        image_url=product_data.image_url,
        category=product_data.category,
        available=product_data.available
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session):
    return db.query(Product).filter(Product.available == True).all()

def get_distinct_values(db: Session, field):
    return [val[0] for val in db.query(field).distinct().all()]

def get_products_by_material(db: Session, material: str):
    return db.query(Product).filter(Product.available == True, Product.material == material).all()

def get_products_by_color(db: Session, color: str):
    return db.query(Product).filter(Product.available == True, Product.color == color).all()

def get_products_by_category(db: Session, category: str):
    return db.query(Product).filter(Product.available == True, Product.category == category).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def seed_admin(db: Session):
    admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if not admin_exists:
        admin = User(
            name="Admin",
            email="admin@example.com",
            hashed_password=hash_password("admin"),  
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()

def seed_products(db: Session):
    existing_products = db.query(Product).count()
    if existing_products > 0:
        return

    sample_products = [ 
    ProductCreate(
        name='Браслет "Бризки неба"',
        price=1200,
        description='Елегантний браслет із натуральними каменями.',
        image_url='/static/images/image 67.png',
        category='bracelets',
        material='gold',  
        color='blue' 
    ),
    ProductCreate(
        name='Кулон "Рожева благодать"',
        price=2400,
        description='Вишуканий кулон у рожевих тонах.',
        image_url='/static/images/image 88.png',
        category='crosses pendants',
        material='silver',  
        color='pink'  
    ),
    ProductCreate(
        name='Каблучка "Місячна соната"',
        price=1350,
        description='Каблучка з місячним сяйвом.',
        image_url='/static/images/image 76.png',
        category='rings',
        material='platinum', 
        color='white'
    ),
    ProductCreate(
        name='Браслет "Рубіновий шепіт"',
        price=2650,
        description='Браслет з рубіновим відтінком.',
        image_url='/static/images/image 68.png',
        category='bracelets',
        material='gold',  
        color='red' 
    ),
    ProductCreate(
        name='Сережки "Аметистове відлуння"',
        price=2700,
        description='Аметистові сережки.',
        image_url='/static/images/image 89.png',
        category='crosses earrings',
        material='silver',  
        color='purple'  
    ),
    ProductCreate(
        name='Каблучка "Королівський шторм"',
        price=3200,
        description='Енергійна каблучка з королівським блиском.',
        image_url='/static/images/image 73.png',
        category='rings',
        material='platinum', 
        color='blue'  
    ),
    ProductCreate(
        name='Каблучка "Смарагдове віче"',
        price=3700,
        description='Яскрава каблучка зі смарагдом.',
        image_url='/static/images/image 90.png',
        category='rings',
        material='gold', 
        color='green' 
    ),
    ProductCreate(
        name='Каблучка "Легенда темного крила"',
        price=2200,
        description='Темна витонченість у каблучці.',
        image_url='/static/images/image 81.png',
        category='rings',
        material='platinum', 
        color='black' 
    ),
    ProductCreate(
        name='Намисто "Смарагдовий ранок"',
        price=1600,
        description='Свіжість ранку в зеленому камені.',
        image_url='/static/images/image 77.png',
        category='chainlet',
        material='gold',
        color='green'  
    ),
    ProductCreate(
        name='Браслет "Сузір’я грації"',
        price=1900,
        description='Ніжний браслет зіркової тематики.',
        image_url='/static/images/image 79.png',
        category='bracelets',
        material='silver', 
        color='white' 
    ),
    ProductCreate(
        name='Кулон "Тихий хрест"',
        price=2150,
        description='Кулон у формі хреста з мінімалістичним дизайном.',
        image_url='/static/images/image 86.png',
        category='crosses pendants',
        material='silver', 
        color='white' 
    ),
    ProductCreate(
        name='Сережки "Чорне серце"',
        price=1790,
        description='Символ глибоких почуттів у сережках.',
        image_url='/static/images/image 69.png',
        category='earrings',
        material='gold', 
        color='black'  
    ),
    ProductCreate(
        name='Підвіска "Сльоза океану"',
        price=2700,
        description='Сяйво океану в підвісці.',
        image_url='/static/images/image 85.png',
        category='pendants',
        material='silver', 
        color='blue'  
    ),
    ProductCreate(
        name='Кольє "Крила янгола"',
        price=3200,
        description='Ніжність у формі крила.',
        image_url='/static/images/image 80.png',
        category='chainlet',
        material='platinum',  
        color='white' 
    ),
    ProductCreate(
        name='Кулон "Подих прозорості"',
        price=3700,
        description='Чистота і прозорість у кожній деталі.',
        image_url='/static/images/image 72.png',
        category='pendants',
        material='platinum',  
        color='white'  
    ),
    ProductCreate(
        name='Ланцюжок "Срібний дельфін"',
        price=2200,
        description='Морська тематика в прикрасі.',
        image_url='/static/images/image 83.png',
        category='chainlet',
        material='silver', 
        color='blue'  
    ),
    ProductCreate(
        name='Сережки "Трояндовий серпанок"',
        price=1600,
        description='Ніжні рожеві сережки.',
        image_url='/static/images/image 70.png',
        category='earrings',
        material='gold', 
        color='pink'  
    ),
    ProductCreate(
        name='Підвіска "Мідне тепло"',
        price=1900,
        description='Теплий відтінок металу.',
        image_url='/static/images/image 78.png',
        category='pendants chainlet',
        material='gold',  
        color='red'  
    ),
    ProductCreate(
        name='Підвіска "Зоряний кристал"',
        price=2150,
        description='Світло зірок у камені.',
        image_url='/static/images/image 82.png',
        category='pendants',
        material='platinum', 
        color='white'  
    ),
    ProductCreate(
        name='Каблучка "Чорна орхідея"',
        price=1790,
        description='Таємнича елегантність.',
        image_url='/static/images/image 75.png',
        category='rings',
        material='gold', 
        color='black'  
    )
]
    for product in sample_products:
        create_product(db, product)
