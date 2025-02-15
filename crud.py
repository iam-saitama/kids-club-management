from sqlalchemy.orm import Session
from models import Admin, Parent, Child, Lesson, Payment, Teacher
from schemas import AdminCreate, ParentCreate, ChildCreateByAdmin, LessonCreate, PaymentCreate, TeacherCreate
from security import get_password_hash


# Создание админа
def create_admin(db: Session, admin: AdminCreate):
    # Проверка на уникальность username
    db_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    if db_admin:
        raise ValueError("Такой username уже существует")

    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(username=admin.username,
                     hashed_password=hashed_password,
                     date_of_birth=admin.date_of_birth)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# Создание учителя
def create_teacher(db: Session, teacher: TeacherCreate):
    # Проверка на уникальность username
    db_teacher = db.query(Teacher).filter(Teacher.username == teacher.username).first()
    if db_teacher:
        raise ValueError("Такой username уже существует")

    hashed_password = get_password_hash(teacher.password)
    db_teacher = Teacher(username=teacher.username,
                         hashed_password=hashed_password,
                         date_of_birth=teacher.date_of_birth)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


# Создание родителя
def create_parent(db: Session, parent: ParentCreate):
    # Проверка на уникальность username
    db_parent = db.query(Parent).filter(Parent.username == parent.username).first()
    if db_parent:
        raise ValueError("Такой username уже существует")

    hashed_password = get_password_hash(parent.password)
    db_parent = Parent(username=parent.username,
                       hashed_password=hashed_password,
                       date_of_birth=parent.date_of_birth)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

# Создание ребенка администратором
def create_child_by_admin(db: Session, child: ChildCreateByAdmin):
    db_child = Child(**child.dict())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

# Добавление ребенка к родителю
def add_child_to_parent(db: Session, parent_id: int, child_id: int):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    child = db.query(Child).filter(Child.id == child_id).first()

    if not parent or not child:
        raise ValueError("Не найдено")

    # Проверка, что ребенок уже не привязан к этому родителю
    if child in parent.children:
        raise ValueError("Этот ребенок уже привязан к Вам")

    parent.children.append(child)
    db.commit()
    return child

# Урок
def create_lesson(db: Session, lesson: LessonCreate):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# Платеж
def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment



