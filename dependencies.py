from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Union
from models import Admin, Parent, Child, Teacher
from database import SessionLocal
from security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Получаем БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Определяем типы/роли пользователей
User = Union[Admin, Parent, Teacher]


# Получаем текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=401,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Выбираем модель в зависимости от роли
    if role == "admin":
        model = Admin
    elif role == "parent":
        model = Parent
    elif role == "teacher":
        model = Teacher
    else:
        raise credentials_exception

    user = db.query(model).filter(model.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# Если нужен админ текущий
def get_current_admin(current_user: User = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="У Вас нет прав администратора")
    return current_user

# Если нужен родитель текущий
def get_current_parent(current_user: User = Depends(get_current_user)):
    if not isinstance(current_user, Parent):
        raise HTTPException(status_code=403, detail="У Вас нет прав родителя")
    return current_user

# Если нужен учитель текущий (лол)
def get_current_teacher(current_user: User = Depends(get_current_user)):
    if not isinstance(current_user, Teacher):
        raise HTTPException(status_code=403, detail="У Вас нет прав учителя")
    return current_user


# Ищем пользователя по username в БД
def get_user_by_username(db: Session, username: str):
    user = db.query(Admin).filter(Admin.username == username).first()
    if not user:
        user = db.query(Teacher).filter(Teacher.username == username).first()
    if not user:
        user = db.query(Parent).filter(Parent.username == username).first()
    return user


"""

Доработать !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""

# Проверка, что родитель имеет доступ к ребенку
def verify_parent_child_access(parent_id: int,
                               child_id: int,
                               db: Session = Depends(get_db),
                               current_parent: Parent = Depends(get_current_parent)):
    if current_parent.id != parent_id:
        raise HTTPException(status_code=403, detail="У Вас нет доступа")

    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Не найдено")

    if child.parent_id != parent_id:
        raise HTTPException(status_code=403, detail="У Вас нет доступа")

    return child

