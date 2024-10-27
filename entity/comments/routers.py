from http.client import HTTPException
from database import get_db
from entity.comments.models import Comment
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from entity.comments.schemas import CommentCreate, CommentUpdate

router = APIRouter()

@router.get("/manga/{manga_id}/chapters/{chapter_id}/comments/")
def read_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    return comments

@router.post("/manga/{manga_id}/chapters/{chapter_id}/comments/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(content=comment.content, mark =comment.mark, user_id=comment.user_id, manga_id=comment.manga_id, chapter_id =comment.chapter_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/manga/{manga_id}/chapters/{chapter_id}/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    return {"detail": "Comment deleted"}

@router.put("/manga/{manga_id}/chapters/{chapter_id}/comments/{comment_id}")
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


     db.commit()
     db.refresh(db_comment)

     return db_comment
