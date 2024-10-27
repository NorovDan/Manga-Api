from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    mark = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    manga_id = Column(Integer, ForeignKey("manga.id"))

    user = relationship("User")
    manga = relationship("Manga")