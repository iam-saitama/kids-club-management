from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import ChildResponse
from crud import add_child_to_parent
from services import find_child_by_search_query


parent_router = APIRouter(prefix="/parent", tags=["parent"])

"""

Доработать

"""

# Добавление ребенка к родителю
# @parent_router.post("/{parent_id}/parent-add-child", response_model=ChildResponse)
# def add_child(parent_id: int,
#               child_data: AddChildToParent,
#               db: Session = Depends(get_db)):
#     child = find_child_by_search_query(db, search_query=child_data.search_query, birth_date=child_data.birth_date)
#     if not child:
#         raise HTTPException(status_code=404, detail="Ребенок не найден или дата рождения не совпадает")
#
#     db_child = add_child_to_parent(db, parent_id=parent_id, child_id=child.id)
#     return JSONResponse(content={"success": True, "child": db_child.dict()})


