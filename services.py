from sqlalchemy.orm import Session
from models import Child, Lesson, Payment, Parent
from schemas import PaymentCreate
from fastapi import HTTPException
import requests
from os import getenv
from datetime import datetime
from fuzzywuzzy import fuzz


# Поиск ребенка по имени, фамилии и дате рождения
def find_child_by_search_query(db: Session, search_query: str,
                               birth_date: datetime):
    children = db.query(Child).all()
    best_match = None
    best_score = 0

    for child in children:
        # Создаем строку для поиска (имя + фамилия на русском и латинице)
        full_name_ru = f"{child.first_name_ru} {child.last_name_ru}"
        full_name_en = f"{child.first_name_en} {child.last_name_en}"

        # Сравниваем поисковый запрос с полным именем
        score_ru = fuzz.ratio(search_query.lower(), full_name_ru.lower())
        score_en = fuzz.ratio(search_query.lower(), full_name_en.lower())
        score = max(score_ru, score_en)

        # Проверяем, совпадает ли дата рождения
        if child.birth_date == birth_date:
            if score > best_score:
                best_score = score
                best_match = child

    # Если совпадение достаточно хорошее
    if best_match and best_score > 80:
        return best_match
    return None

# Добавление ребенка к родителю с проверкой даты рождения
def add_child_to_parent(db: Session, parent_id: int, child_id: int):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise ValueError("Child not found")

    # Привязываем ребенка к родителю
    child.parent_id = parent_id
    child.date_added = datetime.utcnow()
    db.commit()
    db.refresh(child)
    return child


"""

Спросить у Ибрагима про платеж !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


# Обработка платежа
def process_payment(payment_data: PaymentCreate,
                    db: Session,
                    payment_system: str,
                    current_parent: Parent):
    # Проверяем, что ребенок существует
    child = db.query(Child).filter(Child.id == payment_data.child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    # Проверяем, что ребенок принадлежит текущему родителю
    if child.parent_id != current_parent.id:
        raise HTTPException(status_code=403, detail="You can only pay for your own child")

    # Проверяем, что урок существует
    lesson = db.query(Lesson).filter(Lesson.id == payment_data.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Определяем платежную систему
    url = "https://checkout.paycom.uz/api" if payment_system == "payme" else "https://api.click.uz/v2/merchant/invoice/create"
    headers = {
        "X-Auth": getenv("PAYME_MERCHANT_ID") if payment_system == "payme" else getenv("CLICK_SECRET_KEY"),
        "Content-Type": "application/json"
    }

    # Проверяем наличие учетных данных
    if not headers["X-Auth"]:
        raise HTTPException(status_code=500, detail=f"Missing {payment_system.upper()} credentials")

    try:
        response = requests.post(
            url,
            json={
                "amount": int(payment_data.amount * 100),  # Переводим сумму в копейки/тиин
                "account": {"order_id": f"lesson_{payment_data.lesson_id}_child_{payment_data.child_id}"}
            },
            headers=headers,
            timeout=10  # Таймаут для запроса
        )
        response.raise_for_status()  # Проверяем статус ответа
        payment_id = response.json().get("invoice_id") or response.json().get("result", {}).get("card", {}).get("token")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Payment system error: {str(e)}")

    # Проверяем, что платеж с таким payment_id еще не существует
    existing_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists")

    # Создаем запись о платеже
    db_payment = Payment(
        amount=payment_data.amount,
        date=datetime.utcnow(),
        status="pending",
        payment_system=payment_system,
        payment_id=payment_id,
        child_id=payment_data.child_id,
        lesson_id=payment_data.lesson_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return {
        "payment_id": payment_id,
        "amount": payment_data.amount,
        "child_id": payment_data.child_id,
        "lesson_id": payment_data.lesson_id,
        "status": "pending"
    }