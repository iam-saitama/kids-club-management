from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Float, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# Админ
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)



# Учитель
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)
    subject = Column(String)

    # Связь с уроками
    lessons = relationship("Lesson", back_populates="teacher")



# Таблица для связи родителей и детей
child_parent_association = Table(
    "child_parent_association",
    Base.metadata,
    Column("parent_id", ForeignKey("parents.id"), primary_key=True),
    Column("child_id", ForeignKey("children.id"), primary_key=True)
)


# Родитель
class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)


    # Связь с детьми
    children = relationship("Child", secondary=child_parent_association, back_populates="parents")


# Ребенок
class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    first_name_ru = Column(String, index=True)
    last_name_ru = Column(String, index=True)
    first_name_en = Column(String, index=True)
    last_name_en = Column(String, index=True)
    date_of_birth = Column(Date)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="children")
    lessons = relationship("ChildLesson", back_populates="child")
    payments = relationship("Payment", back_populates="child")
    date_added = Column(DateTime, default=datetime.utcnow)

    # Связь с родителями
    parents = relationship("Parent", secondary=child_parent_association, back_populates="children")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    day_of_week = Column(String)
    time = Column(Time)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    monthly_price = Column(Float, default=0.0)

    teacher = relationship("Teacher", back_populates="lessons")
    children = relationship("ChildLesson", back_populates="lesson")
    payments = relationship("Payment", back_populates="lesson")

class ChildLesson(Base):
    __tablename__ = "child_lessons"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    child = relationship("Child", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="children")


"""

Спросить у Ибрагима про платеж !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(DateTime)
    status = Column(String, default="pending")
    payment_system = Column(String)
    payment_id = Column(String)
    child_id = Column(Integer, ForeignKey("children.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    child = relationship("Child", back_populates="payments")
    lesson = relationship("Lesson", back_populates="payments")


