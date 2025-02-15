from pydantic import BaseModel, ConfigDict, constr
from datetime import date, time, datetime
from typing import List

# Админ
class AdminBase(BaseModel):
    username: str
    date_of_birth: date

class AdminCreate(AdminBase):
    password: str
    is_super_admin: bool = False

class AdminResponse(AdminBase):
    id: int
    is_super_admin: bool
    model_config = ConfigDict(from_attributes=True)


# Учитель
class TeacherBase(BaseModel):
    username: constr(min_length=3, max_length=20)
    phone: constr(min_length=10, max_length=15)
    date_of_birth: date
    subject: str

class TeacherCreate(TeacherBase):
    password: constr(min_length=8)

class TeacherResponse(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Родитель
class ParentBase(BaseModel):
    username: constr(min_length=3, max_length=20)
    phone: constr(min_length=10, max_length=15)
    date_of_birth: date

class ParentCreate(ParentBase):
    password: constr(min_length=8)

class ParentResponse(ParentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Ребенок
class ChildBase(BaseModel):
    name_ru: str
    name_en: str
    date_of_birth: date

class ChildCreateByAdmin(ChildBase):
    last_name_ru: str
    last_name_en: str

class ChildResponse(ChildBase):
    id: int
    parent_ids: List[int]
    model_config = ConfigDict(from_attributes=True)


# Добавление ребенка к родителю
class AddChildToParent(BaseModel):
    search_query: str


# Урок
class LessonBase(BaseModel):
    name: str
    day_of_week: str
    time: time
    monthly_price: float

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    teacher_id: int

    model_config = ConfigDict(from_attributes=True)


"""

Спросить у Ибрагима про платеж !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


# Платеж
class PaymentBase(BaseModel):
    amount: float
    date: datetime
    child_id: int
    lesson_id: int

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)





