import os
import redis
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from fastapi import HTTPException
from .config import settings


class BaseRepository:
    def create(self, full_name: str):
        raise NotImplementedError

    def get(self, user_id: int):
        raise NotImplementedError

    def update(self, user_id: int, full_name: str):
        raise NotImplementedError

    def delete(self, user_id: int):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError


class ORMRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, full_name: str):
        user = User(full_name=full_name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: int, full_name: str):
        user = self.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.full_name = full_name
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()

    def list(self):
        return self.db.query(User).all()


class RedisRepository(BaseRepository):
    def __init__(self, redis_client):
        self.redis = redis_client
        self.counter = 0

    def create(self, full_name: str):
        user_id = self.counter
        self.redis.hmset(f"user:{user_id}", {"id": user_id, "full_name": full_name})
        self.counter += 1
        return {"id": user_id, "full_name": full_name}

    def get(self, user_id: int):
        user = self.redis.hgetall(f"user:{user_id}")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update(self, user_id: int, full_name: str):
        if not self.redis.exists(f"user:{user_id}"):
            raise HTTPException(status_code=404, detail="User not found")
        self.redis.hmset(f"user:{user_id}", {"full_name": full_name})
        return self.get(user_id)

    def delete(self, user_id: int):
        if not self.redis.exists(f"user:{user_id}"):
            raise HTTPException(status_code=404, detail="User not found")
        self.redis.delete(f"user:{user_id}")

    def list(self):
        keys = self.redis.keys("user:*")
        return [self.redis.hgetall(key) for key in keys]


def get_repository(db: Session = None):
    if settings.REPOSITORY_TYPE == 'orm':
        return ORMRepository(db)
    elif settings.REPOSITORY_TYPE == 'redis':
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        return RedisRepository(redis_client)
    else:
        raise ValueError("Unknown repository type")
