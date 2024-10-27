from http.client import HTTPException
from database import get_db
from entity.chapters.models import Chapter
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from entity.chapters.schemas import ChapterCreate, ChapterUpdate

router = APIRouter()

@router.put("/manga/{manga_id}/chapters/{chapter_id}")
def update_chapter(chapter_id: int, chapter: ChapterUpdate, db: Session = Depends(get_db)):
     db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

     if not db_chapter:
         raise HTTPException(status_code=404, detail="Chapter not found")

     if chapter.rate is not None:
         db_chapter.rate = chapter.rate
     if chapter.chapter_itself is not None:
         db_chapter.chapter_itself = chapter.chapter_itself
     if chapter.manga_id is not None:
         db_chapter.manga_id = chapter.manga_id
     if chapter.user_id is not None:
         db_chapter.user_id = chapter.user_id

     db.commit()
     db.refresh(db_chapter)

     return db_chapter

@router.get("/manga/{manga_id}/chapters/")
def read_chapters(db: Session = Depends(get_db)):
    chapters = db.query(Chapter).all()
    return chapters

@router.post("/chapters/")
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db), db_chapter=None):
    db_chapter = Chapter(rate=chapter.rate, chapter_itself =chapter.chapter_itself, user_id=chapter.user_id, manga_id=chapter.manga_id)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

@router.delete("/manga/{manga_id}/chapters/{chapter_id}")
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    db.delete(db_chapter)
    db.commit()
    return {"detail": "Chapter deleted"}