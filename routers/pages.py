# Шаблоны здесь

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config import templates
from datetime import datetime
import locale

page_router = APIRouter()

# Устанавливаем русскую локаль
locale.setlocale(locale.LC_TIME, "ru_RU.utf8")

# Главная страница
@page_router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Страница логина
@page_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Страница выбора роли
@page_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Страница регистрации учителя
@page_router.get("/register/teacher", response_class=HTMLResponse)
def register_teacher_page(request: Request):
    return templates.TemplateResponse("register_teacher.html", {"request": request})

# Страница регистрации родителя
@page_router.get("/register/parent", response_class=HTMLResponse)
def register_parent_page(request: Request):
    return templates.TemplateResponse("register_parent.html", {"request": request})

# Страница создания урока
@page_router.get("/create", response_class=HTMLResponse)
def create_lesson_page(request: Request):
    return templates.TemplateResponse("create_lesson.html", {"request": request})

# Страница добавления ребенка
@page_router.get("/add-child", response_class=HTMLResponse)
def add_child_page(request: Request):
    today = datetime.today()
    formatted_date = today.strftime("%d %B %Y")
    return templates.TemplateResponse("add_child.html", {"request": request, "formatted_date": formatted_date})

# Страница оплаты
@page_router.get("/payment", response_class=HTMLResponse)
def payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})



