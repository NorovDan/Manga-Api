from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    mark = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    manga_id = Column(Integer, ForeignKey("manga.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))

    user = relationship("User")
    manga = relationship("Manga")
    chapter = relationship("Chapter")