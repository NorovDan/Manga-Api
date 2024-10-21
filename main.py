from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.orm import Session
from models import SessionLocal, Manga, User, Review, Chapter, Comment
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

class MangaCreate(BaseModel):
    title: str
    author: str
    publisher: str
    description: str
    rate: float
    image: str  # URL или путь к изображению
    genre: str
    amount: int

class MangaUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    rate: Optional[float] = None
    image: Optional[str] = None
    genre: Optional[str] = None
    amount: Optional[int] = None

class ReviewCreate(BaseModel):
    content: str
    mark: int
    user_id: int
    manga_id: int

class CommentCreate(BaseModel):
    content: str
    mark: int
    user_id: int
    manga_id: int
    chapter_id: int

class ChapterCreate(BaseModel):
    rate: float
    chapter_itself: str
    user_id: int
    manga_id: int

class ChapterUpdate(BaseModel):
    rate: Optional[float] = None
    chapter_itself: Optional[str] = None
    user_id: Optional[int] = None
    manga_id: Optional[int] = None

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    mark: Optional[int] = None
    user_id: Optional[int] = None
    manga_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    mark: Optional[int] = None
    user_id: Optional[int] = None
    manga_id: Optional[int] = None
    chapter_id: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существующего пользователя
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Создание нового пользователя
    new_user = User(username=user.username, password_hash=get_password_hash(user.password))

    # Добавление в сессию и коммит
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username}

@app.get("/user/{user_id}")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/manga/{manga_id}/chapters/{chapter_id}/comments/")
def read_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    return comments

@app.get("/reviews/")
def read_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews

@app.get("/manga/{manga_id}/chapters/")
def read_chapters(db: Session = Depends(get_db)):
    chapters = db.query(Chapter).all()
    return chapters

@app.post("/chapters/")
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db), db_chapter=None):
    db_chapter = Chapter(rate=chapter.rate, chapter_itself =chapter.chapter_itself, user_id=chapter.user_id, manga_id=chapter.manga_id)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

@app.post("/manga/")
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


@app.delete("/manga/{manga_id}/")
def delete_manga(manga_id: int, db: Session = Depends(get_db)):
    db_manga = db.query(Manga).filter(Manga.id == manga_id).first()
    if db_manga is None:
        raise HTTPException(status_code=404, detail="Manga not found")

    db.delete(db_manga)
    db.commit()
    return {"detail": "Manga deleted"}

@app.delete("/manga/{manga_id}/chapters/{chapter_id}/")
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    db.delete(db_chapter)
    db.commit()
    return {"detail": "Chapter deleted"}

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted"}

@app.delete("/manga/{manga_id}/chapters/{chapter_id}/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    return {"detail": "Comment deleted"}

@app.put("/manga/{manga_id}")
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

@app.put("/manga/{manga_id}/chapters/{chapter_id}")
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

@app.put("/reviews/{review_id}")
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
     db_review = db.query(Review).filter(Review.id == review_id).first()

     if not db_review:
         raise HTTPException(status_code=404, detail="Review not found")

     if review.content is not None:
         db_review.content = review.content
     if review.mark is not None:
         db_review.mark = review.mark
     if review.user_id is not None:
         db_review.user_id = review.user_id
     if review.manga_id is not None:
         db_review.manga_id = review.manga_id


     db.commit()
     db.refresh(db_review)

     return db_review

@app.put("/manga/{manga_id}/chapters/{chapter_id}/comments/{comment_id}")
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
     db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

     if not db_comment:
         raise HTTPException(status_code=404, detail="Comment not found")

     if comment.content is not None:
         db_comment.text = comment.content
     if comment.mark is not None:
         db_comment.mark = comment.mark
     if comment.user_id is not None:
         db_comment.user_id = comment.user_id
     if comment.manga_id is not None:
         db_comment.manga_id = comment.manga_id
     if comment.chapter_id is not None:
         db_comment.chapter_id =comment.chapter_id

@app.post("/reviews/")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(content=review.content, mark =review.mark, user_id=review.user_id, manga_id=review.manga_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.post("/manga/{manga_id}/chapters/{chapter_id}/comments/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(content=comment.content, mark =comment.mark, user_id=comment.user_id, manga_id=comment.manga_id, chapter_id =comment.chapter_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/manga/{manga_id}/reviews/")
def read_reviews(manga_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.manga_id == manga_id).all()
    return reviews

@app.get("/manga/")
def read_manga(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mangas = db.query(Manga).offset(skip).limit(limit).all()
    return mangas

@app.get("/")
def home_page():
    return {"message": "Добро пожаловать на Manga Api!"}
