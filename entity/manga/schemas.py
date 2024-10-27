from typing import Optional
from pydantic import BaseModel

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