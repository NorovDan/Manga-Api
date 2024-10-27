from http.client import HTTPException
from database import get_db
from entity.reviews.models import Review
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from entity.reviews.schemas import ReviewCreate, ReviewUpdate

router = APIRouter()

@router.post("/reviews/")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(content=review.content, mark =review.mark, user_id=review.user_id, manga_id=review.manga_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/manga/{manga_id}/reviews/")
def read_reviews(manga_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.manga_id == manga_id).all()
    return reviews

@router.get("/reviews/")
def read_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews





@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted"}



@router.put("/reviews/{review_id}")
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