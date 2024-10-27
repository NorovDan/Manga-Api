from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from entity.users.models import User

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Float)
    chapter_itself = Column(String)  # URL или путь к изображению
    user_id = Column(Integer, ForeignKey("users.id"))
    manga_id = Column(Integer, ForeignKey("manga.id"))

