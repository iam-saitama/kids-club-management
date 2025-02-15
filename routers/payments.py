from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_parent
from schemas import PaymentCreate
from services import process_payment
from models import Parent

payment_router = APIRouter(prefix="/payments", tags=["payments"])


"""

Спросить у Ибрагима про платеж !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


# Создание платежа через Payme
@payment_router.post("/payme/create")
def create_payme_payment(payment_data: PaymentCreate,
                         db: Session = Depends(get_db),
                         current_parent: Parent = Depends(get_current_parent)):

    payment = process_payment(payment_data, db, "payme", current_parent)
    return JSONResponse(content={"success": True, "payment": payment.dict()})

# Создание платежа через Click
@payment_router.post("/click/create")
def create_click_payment(payment_data: PaymentCreate,
                         db: Session = Depends(get_db),
                         current_parent: Parent = Depends(get_current_parent)):

    payment = process_payment(payment_data, db, "click", current_parent)
    return JSONResponse(content={"success": True, "payment": payment.dict()})

