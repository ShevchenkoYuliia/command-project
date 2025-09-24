
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import List
from app.models import UserRole, User
from app.database import get_current_user


security = HTTPBearer(auto_error=False)

def get_user_role(current_user):
    return current_user.role

def role_required(allowed_roles: List[UserRole]):
    def dependency(current_user: User = Depends(get_current_user)):
        if not current_user or current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостатньо прав для доступу до цієї сторінки",
            )
        return current_user
    return Depends(dependency)
