from fastapi import FastAPI

from typing import Optional

from controllers import create_user, create_user_item
from database import SessionLocal, engine
from models import Base, Item, ItemHistory
from schemas import UserCreate, ItemCreate, UserId

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "Azure"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/users/")
def create_user_endpoint(user: UserCreate):
    db = SessionLocal()
    return create_user(user=user)


@app.post("/users/{user_id}/items/")
def create_item_for_user(user_id: int, item: ItemCreate):
    db = SessionLocal()
    return create_user_item(item=item, user_id=user_id)


@app.post("/reassign_item/{item_id}/")
def assign_item(item_id: int, new_owner: UserId):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    item.owner_id = new_owner.id
    db.add(item)
    db.commit()
    add_history(db, item, new_owner.id)


def add_history(db, item, new_owner_id):
    history_entry = ItemHistory(
        item_id=item.id,
        old_assignee=item.owner_id,
        new_assignee=new_owner_id
    )
    db.add(history_entry)
    db.commit()
