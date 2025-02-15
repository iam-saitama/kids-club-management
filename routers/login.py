from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_user_by_username
from security import verify_password

login_router = APIRouter(prefix="/login", tags=["login"])

# Логин для всех. Роль (учитель/родитель/админ) определяет по юзернейму
@login_router.post("/login", response_class=JSONResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильное имя пользователя или пароль")

    return JSONResponse(
        content={"success": True, "message": "Успешный вход", "user_id": user.id})



