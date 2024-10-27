from sqlalchemy import  Column, Integer, String,  Float
from database import Base

class Manga(Base):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    publisher = Column(String)
    description = Column(String)
    rate = Column(Float)
    image = Column(String)  # URL или путь к изображению
    genre = Column(String)
    amount = Column(Integer)