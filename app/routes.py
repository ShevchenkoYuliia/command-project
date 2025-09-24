from fastapi import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import *
from app.models import Order, User, Product 
from app.schemas import UserCreate, OrderCreate, OrderItemCreate
import json
from typing import List
from datetime import datetime
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
from app.auth import role_required

@router.get("/", response_class=HTMLResponse)
async def root(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "user": current_user}
    )

@router.get("/index", response_class=HTMLResponse)
async def index_redirect(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "user": current_user}
    )
@router.get("/cart", response_class=HTMLResponse)
async def show_cart(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("cart.html", {"request": request})

@router.get("/details/{product_id}", response_class=HTMLResponse)
async def show_product_detail(request: Request, product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    product = get_product_by_id(db, product_id)
    if not product:
        return RedirectResponse(url="/catalog")
    return templates.TemplateResponse("details.html", {"request": request, "product": product, "user": current_user})

@router.get("/catalog", response_class=HTMLResponse)
async def show_catalog(
    request: Request, 
    category: str = Query(default=None),
    material: str = Query(default=None),
    color: str = Query(default=None),
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    query = db.query(Product).filter(Product.available == True)

    if category:
        query = query.filter(Product.category == category)
    if material:
        query = query.filter(Product.material == material)
    if color:
        query = query.filter(Product.color == color)

    products = query.all()
    categories = get_distinct_values(db, Product.category)
    materials = get_distinct_values(db, Product.material)
    colors = get_distinct_values(db, Product.color)


    return templates.TemplateResponse(
        "catalog.html", 
        {
            "request": request, 
            "products": products, 
            "user": current_user,
            "categories": categories,
            "materials": materials,
            "colors": colors,
            "selected_category": category,
            "selected_material": material,
            "selected_color": color
        }
    )

@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    current_user: User = role_required([UserRole.ADMIN]),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    orders = db.query(Order).all()
    products = db.query(Product).all()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": current_user,
            "users": users,
            "orders": orders,
            "products": products
        }
    )

@router.post("/add-user/")
async def add_product(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: UserRole = Form(...),
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(password)
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,  
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url="/admin", status_code=303)
@router.post("/update-user/{user_id}")
async def update_user(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    role: UserRole = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = name
    user.email = email
    user.role = role

    db.commit()
    return RedirectResponse(url="/admin", status_code=303)
@router.post("/delete-user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    return RedirectResponse(url="/admin", status_code=303)
@router.post("/update-product/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    material: str = Form(...),
    color: str = Form(...),
    available: str = Form(...),
    image: str = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name
    product.description = description
    product.price = price
    product.category = category
    product.material = material
    product.color = color
    product.available = (available.lower() == "on")
    product.image_url = image

    db.commit()
    db.refresh(product)

    return RedirectResponse(url="/admin", status_code=303)

@router.post("/add-product/")
async def add_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    material: str = Form(...),
    color: str = Form(...),
    available: str = Form(...),
    image: str = Form(...),
    db: Session = Depends(get_db)
):

    product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        material=material,
        color=color,
        available=(available.lower() == "on"),
        image_url=image 
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return RedirectResponse(url="/admin", status_code=303)

@router.post("/delete-product/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()

    return RedirectResponse(url="/admin", status_code=303)
@router.post("/update-order/{order_id}")
async def update_order(
    order_id: int,
    user_id: str = Form(...),
    total_price: float = Form(...),
    status: str = Form(...),
    created_at: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    payment_method: str = Form(...),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    created_at_datetime = datetime.strptime(created_at, '%Y-%m-%dT%H:%M')
    order.id = order_id
    order.user_id = user_id
    order.total_price = total_price 
    order.status = status
    order.created_at = created_at_datetime
    order.phone = phone
    order.address = address
    order.payment_method = payment_method

    db.commit()
    db.refresh(order)

    return RedirectResponse(url="/admin", status_code=303)


@router.get("/products/simple", response_model=List[dict])
def get_simple_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.available == True).all()
    return [{"id": product.id, "name": product.name} for product in products]

@router.get("/registration", response_class=HTMLResponse)
async def show_register(request: Request, current_user=Depends(get_current_user)):
    if current_user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("registration.html", {"request": request})
@router.post("/register/")
async def register_user(
    request: Request,
    response: Response,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return templates.TemplateResponse(
                "email_already_registered.html", 
                {"request": request, "error": "Already registered with this email"},
                status_code=400
            )

        user_data = UserCreate(name=name, email=email, password=password, role="user")
        user = create_user(db, user_data)

        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="user_id", 
            value=str(user.id),
            httponly=True, 
            max_age=3600,   
            path="/"
        )
        
        return response

    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error": f"Error: {str(e)}"}
        )
    
@router.post("/login/")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "login_error": "Wrong email or password"},
            status_code=401
        )
    
    response = RedirectResponse(url="/", status_code=303)
    
    response.set_cookie(
        key="user_id", 
        value=str(user.id),
        httponly=True,  
        max_age=3600,   
        path="/"
    )
    
    return response

@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="user_id", path="/")
    return response

@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request, current_user=Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/registration?next=/checkout", status_code=303)
    
    return templates.TemplateResponse("checkout.html", {"request": request, "user": current_user})

@router.post("/place-order")
async def place_order(
    request: Request,
    phone: str = Form(...),
    address: str = Form(...),
    orderItems: str = Form(...),
    totalPrice: float = Form(...),
    current_user=Depends(get_current_user),
    payment_method: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        items_data = json.loads(orderItems)
        
        if not items_data:
            return templates.TemplateResponse(
                "checkout.html", 
                {"request": request, "user": current_user, "error": "Cart is empty"}
            )
        
        order_items = []
        for item in items_data:
            order_item = OrderItemCreate(
                product_id=item['product_id'],
                product_name=item['product_name'],
                price=item['price'],
                quantity=item['quantity']
            )
            order_items.append(order_item)
        
        order_data = OrderCreate(
            total_price=totalPrice,
            phone=phone,
            address=address,
            payment_method=payment_method, 
            items=order_items
        )
        user_id = current_user.id if current_user else None
        order = create_order(db, order_data, user_id)
        
        response = RedirectResponse(url="/order-success?id={}".format(order.id), status_code=303)
        return response
        
    except Exception as e:
        return templates.TemplateResponse(
            "checkout.html", 
            {"request": request, "user": current_user, "error": f"Error when placing an order: {str(e)}"}
        )

@router.get("/order-success", response_class=HTMLResponse)
async def order_success(
    request: Request, 
    id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order_by_id(db, id)
    
    if not order:
        return RedirectResponse(url="/", status_code=303)
    
    if order.user_id and current_user and order.user_id != current_user.id:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse(
        "order-success.html", 
        {"request": request, "user": current_user, "order": order}
    )

@router.get("/my-orders", response_class=HTMLResponse)
async def my_orders(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        return RedirectResponse(url="/registration?next=/my-orders", status_code=303)
    
    orders = get_user_orders(db, current_user.id)
    
    return templates.TemplateResponse(
        "orders.html", 
        {"request": request, "user": current_user, "orders": orders}
    )