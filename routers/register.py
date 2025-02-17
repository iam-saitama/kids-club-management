from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_user_by_username
from schemas import ParentCreate, TeacherCreate
from crud import create_parent, create_teacher


register_router = APIRouter(prefix="/register", tags=["register"])

# Регистрация родителя
@register_router.post("/parent", response_class=JSONResponse)
def register_parent(parent: ParentCreate,
                    db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким username
    db_parent = get_user_by_username(db, username=parent.username)
    if db_parent:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято.")

    # Создаем нового родителя
    new_parent = create_parent(db=db, parent=parent)
    return {"success": True, "message": "Родитель успешно зарегистрирован.", "parent_id": new_parent.id}


# Регистрация учителя
@register_router.post("/teacher", response_class=JSONResponse)
def register_teacher(teacher: TeacherCreate,
                     db: Session = Depends(get_db)):
    db_teacher = get_user_by_username(db, username=teacher.username)
    if db_teacher:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято.")

    new_teacher = create_teacher(db=db, teacher=teacher)
    return JSONResponse(
        content={"success": True, "message": "Учитель успешно зарегистрирован.", "teacher_id": new_teacher.id})


