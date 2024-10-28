from fastapi import FastAPI
from entity.manga.routers import router as router_manga
from entity.chapters.routers import router as router_chapter
from entity.comments.routers import router as router_comment
from entity.reviews.routers import router as router_review
from entity.users.routers import router as router_user

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Добро пожаловать на Manga Api!"}

app.include_router(router_manga)
app.include_router(router_chapter)
app.include_router(router_comment)
app.include_router(router_review)
app.include_router(router_user)
