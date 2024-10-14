from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./manga.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)



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

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Float)
    chapter_itself = Column(String)  # URL или путь к изображению
    user_id = Column(Integer, ForeignKey("users.id"))
    manga_id = Column(Integer, ForeignKey("manga.id"))

    user = relationship("User")
    manga = relationship("Manga")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    mark = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    manga_id = Column(Integer, ForeignKey("manga.id"))

    user = relationship("User")
    manga = relationship("Manga")

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

Base.metadata.create_all(bind=engine)













