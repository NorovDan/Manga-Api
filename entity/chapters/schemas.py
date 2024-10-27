from typing import Optional
from pydantic import BaseModel

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