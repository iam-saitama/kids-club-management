from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_user_by_username
from models import Admin
from fastapi.security import OAuth2PasswordRequestForm

register_router = APIRouter(prefix="/admin", tags=["admin"])


# Регистрация админа
@register_router.post("/register", response_class=JSONResponse)
def register_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Проверка на уникальность username
    existing_user = get_user_by_username(db, form_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такой username уже существует")

    db_admin = Admin(username=form_data.username, hashed_password=form_data.password, is_super_admin=False)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return JSONResponse(content={"success": True,
                                 "message": "Админ зарегистрирован",
                                 "username": db_admin.username,
                                 "is_super_admin": db_admin.is_super_admin})
