from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import LessonCreate, LessonResponse
from crud import create_lesson


lesson_router = APIRouter(prefix="/lessons", tags=["lessons"])


"""

Доработать !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""


# Создание урока
@lesson_router.post("/", response_model=LessonResponse)
def create_lesson_api(lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = create_lesson(db=db, lesson=lesson)
    return JSONResponse(content={"success": True, "lesson": db_lesson.dict()})

