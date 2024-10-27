from typing import Optional
from pydantic import BaseModel

class ReviewCreate(BaseModel):
    content: str
    mark: int
    user_id: int
    manga_id: int

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    mark: Optional[int] = None
    user_id: Optional[int] = None
    manga_id: Optional[int] = None