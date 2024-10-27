from http.client import HTTPException
from database import get_db
from entity.manga.models import Manga
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from entity.manga.schemas import MangaCreate, MangaUpdate

router = APIRouter()

@router.post("/manga")
def create_manga(manga: MangaCreate, db: Session = Depends(get_db)):
    db_manga = Manga(
        title=manga.title,
        author=manga.author,
        publisher=manga.publisher,
        description=manga.description,
        rate=manga.rate,
        image=manga.image,
        genre=manga.genre,
        amount=manga.amount
    )
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga

@router.delete("/manga/{manga_id}")
def delete_manga(manga_id: int, db: Session = Depends(get_db)):
    db_manga = db.query(Manga).filter(Manga.id == manga_id).first()
    if db_manga is None:
        raise HTTPException(status_code=404, detail="Manga not found")

    db.delete(db_manga)
    db.commit()
    return {"detail": "Manga deleted"}

@router.put("/manga/{manga_id}")
def update_manga(manga_id: int, manga: MangaUpdate, db: Session = Depends(get_db)):
    db_manga = db.query(Manga).filter(Manga.id == manga_id).first()

    if not db_manga:
        raise HTTPException(status_code=404, detail="Manga not found")

    if manga.title is not None:
        db_manga.title = manga.title
    if manga.author is not None:
        db_manga.author = manga.author
    if manga.publisher is not None:
        db_manga.publisher = manga.publisher
    if manga.description is not None:
        db_manga.description = manga.description
    if manga.rate is not None:
        db_manga.rate = manga.rate
    if manga.image is not None:
        db_manga.image = manga.image
    if manga.genre is not None:
        db_manga.genre = manga.genre
    if manga.amount is not None:
        db_manga.amount = manga.amount

    db.commit()
    db.refresh(db_manga)

    return db_manga

@router.get("/manga")
def read_manga(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mangas = db.query(Manga).offset(skip).limit(limit).all()
    return mangas