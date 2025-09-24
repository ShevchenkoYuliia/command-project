import pytest
from httpx import AsyncClient
from fastapi import status
from __init__ import app 

@pytest.mark.asyncio
async def test_root_route():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]

@pytest.mark.asyncio
async def test_index_redirect():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/index")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_show_cart():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cart")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_show_product_detail():
    product_id = 1
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/details/{product_id}")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT]

@pytest.mark.asyncio
async def test_show_catalog():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/catalog")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_admin_panel_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/admin")
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

@pytest.mark.asyncio
async def test_add_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123",
            "role": "user"
        }
        response = await ac.post("/add-user/", data=data)
    assert response.status_code in [status.HTTP_303_SEE_OTHER, status.HTTP_401_UNAUTHORIZED]

@pytest.mark.asyncio
async def test_update_user_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "name": "New Name",
            "email": "newemail@example.com",
            "role": "user"
        }
        response = await ac.post("/update-user/99999", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_delete_user_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/delete-user/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_update_product_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "name": "Test",
            "description": "Desc",
            "price": 9.99,
            "category": "cat",
            "material": "mat",
            "color": "red",
            "available": "on",
            "image": "image.jpg"
        }
        response = await ac.post("/update-product/99999", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_add_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "name": "Product Test",
            "description": "Description",
            "price": 10.5,
            "category": "cat",
            "material": "mat",
            "color": "blue",
            "available": "on",
            "image": "img.jpg"
        }
        response = await ac.post("/add-product/", data=data)
    assert response.status_code in [status.HTTP_303_SEE_OTHER, status.HTTP_401_UNAUTHORIZED]

@pytest.mark.asyncio
async def test_delete_product_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/delete-product/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_update_order_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "user_id": "1",
            "total_price": 100.0,
            "status": "new",
            "created_at": "2025-05-21T12:00",
            "phone": "123456789",
            "address": "Some address",
            "payment_method": "card"
        }
        response = await ac.post("/update-order/99999", data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_simple_products():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/products/simple")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_show_register_redirect_if_logged_in():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/registration")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_307_TEMPORARY_REDIRECT]

@pytest.mark.asyncio
async def test_register_user_email_already_registered():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {
            "name": "Test",
            "email": "already@registered.com",
            "password": "password"
        }
        await ac.post("/register/", data=data)
        response = await ac.post("/register/", data=data)

    assert response.status_code in (400, 409)
    assert "email" in response.text.lower()

@pytest.mark.asyncio
async def test_login_wrong_credentials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"email": "wrong@example.com", "password": "wrong"}
        response = await ac.post("/login/", data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "invalid" in response.text.lower() or "wrong" in response.text.lower()
@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_data = {
            "name": "User",
            "email": "login@example.com",
            "password": "secure123"
        }
        await ac.post("/register/", data=register_data)

        login_data = {"email": "login@example.com", "password": "secure123"}
        response = await ac.post("/login/", data=login_data)

    assert response.status_code == status.HTTP_303_SEE_OTHER


@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/logout")
    assert response.status_code == status.HTTP_303_SEE_OTHER
@pytest.mark.asyncio
async def test_checkout_redirect_if_not_logged_in():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/checkout")
    assert response.status_code == status.HTTP_303_SEE_OTHER

@pytest.mark.asyncio
async def test_order_success_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/order-success?id=99999")
    assert response.status_code == status.HTTP_303_SEE_OTHER