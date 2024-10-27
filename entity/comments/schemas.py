from typing import Optional
from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str
    mark: int
    user_id: int
    manga_id: int
    chapter_id: int

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    mark: Optional[int] = None
    user_id: Optional[int] = None
    manga_id: Optional[int] = None
    chapter_id: Optional[int] = None