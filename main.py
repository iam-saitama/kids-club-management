from fastapi import FastAPI
from routers.pages import page_router
from routers.register import register_router
from routers.login import login_router
from routers.teachers import teacher_router
from routers.parents import parent_router
from routers.children import child_router
from routers.lessons import lesson_router
from routers.payments import payment_router
from database import Base, engine
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(page_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(teacher_router)
app.include_router(parent_router)
app.include_router(child_router)
app.include_router(lesson_router)
app.include_router(payment_router)

# Настройка статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


