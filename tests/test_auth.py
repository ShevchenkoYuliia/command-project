import pytest
from fastapi import HTTPException, status
from app.auth import get_user_role, role_required
from app.models import UserRole, User
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from app.auth import get_current_user 


# Моки
class MockUser:
    def __init__(self, role):
        self.role = role

def test_get_user_role_user():
    user = MockUser(UserRole.USER)
    assert get_user_role(user) == UserRole.USER

def test_get_user_role_admin():
    user = MockUser(UserRole.ADMIN)
    assert get_user_role(user) == UserRole.ADMIN

# Тест перевірки доступу на маршрут
def test_role_required_allows_valid_role():
    app = FastAPI()

    @app.get("/admin")
    def read_admin(user: User = role_required([UserRole.ADMIN])):
        return {"msg": "OK"}

    client = TestClient(app)

    # Заміна get_current_user на фейкову функцію, що повертає адміна

    app.dependency_overrides[get_current_user] = lambda: MockUser(UserRole.ADMIN)
    response = client.get("/admin")
    assert response.status_code == 200
    assert response.json() == {"msg": "OK"}

def test_role_required_rejects_invalid_role():
    app = FastAPI()

    @app.get("/admin")
    def read_admin(user: User = role_required([UserRole.ADMIN])):
        return {"msg": "OK"}

    client = TestClient(app)
    
    app.dependency_overrides[get_current_user] = lambda: MockUser(UserRole.USER)

    response = client.get("/admin")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Недостатньо прав" in response.json()["detail"]
