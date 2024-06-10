from database import SessionLocal
from models import User, Item
from schemas import UserCreate, ItemCreate


def create_user(user: UserCreate):
    db = SessionLocal()
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    return db_user


def create_user_item(item: ItemCreate, user_id: int):
    db = SessionLocal()
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    return db_item
