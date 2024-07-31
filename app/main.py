from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import SessionLocal, User
from typing import List
from .schemas import UserCreate, User as UserSchema
from .repositories import get_repository
from .config import settings

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repository = get_repository(db)
    return repository.create(user.full_name)


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    repository = get_repository(db)
    db_user = repository.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    repository = get_repository(db)
    return repository.update(user_id, user.full_name)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repository = get_repository(db)
    repository.delete(user_id)
    return {"ok": True}


@app.get("/users/", response_model=List[UserSchema])
def list_users(db: Session = Depends(get_db)):
    repository = get_repository(db)
    return repository.list()
