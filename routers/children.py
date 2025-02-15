from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import ChildCreateByAdmin, ChildResponse
from crud import create_child_by_admin

child_router = APIRouter(prefix="/children", tags=["children"])


"""

Доработать !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


# Создание ребенка администратором
@child_router.post("/admin/create", response_model=ChildResponse)
def create_child(child: ChildCreateByAdmin, db: Session = Depends(get_db)):
    db_child = create_child_by_admin(db=db, child=child)
    return JSONResponse(content={"success": True, "child": db_child.dict()})


