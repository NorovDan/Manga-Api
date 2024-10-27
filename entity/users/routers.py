from http.client import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import get_db
from entity.users.models import User
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from entity.users.schemas import UserCreate
from entity.users.auth import get_password_hash,get_user,oauth2_scheme, verify_password
router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существующего пользователя
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Создание нового пользователя
    new_user = User(username=user.username,email =user.email, password_hash=get_password_hash(user.password))

    # Добавление в сессию и коммит
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user

@router.get("/user/{user_id}")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users