import os

from sqlalchemy.orm import Session

from models import User, Item, ItemHistory
from schemas import UserCreate, ItemCreate, UserId, Status
from dotenv import load_dotenv

load_dotenv()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + os.getenv("PASSWORD_HASH")
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    return db_item


def add_owner_history(db: Session, item: Item, new_owner_id: int):
    history_entry = ItemHistory(
        item_id=item.id,
        old_assignee_id=item.owner_id,
        new_assignee_id=new_owner_id,
        old_status=item.status,
        new_status=item.status,
    )
    db.add(history_entry)


def reassign_item(db: Session, item_id: int, new_owner: UserId):
    item = db.query(Item).filter(Item.id == item_id).first()
    add_owner_history(db, item, new_owner.id)
    item.owner_id = new_owner.id
    db.add(item)
    db.commit()
    return item


def add_status_history(db: Session, item: Item, new_status: str):
    history_entry = ItemHistory(
        item_id=item.id,
        old_assignee_id=item.owner_id,
        new_assignee_id=item.owner_id,
        old_status=item.status,
        new_status=new_status,
    )
    db.add(history_entry)


def change_item_status(db: Session, item_id: int, status: Status):
    item = db.query(Item).filter(Item.id == item_id).first()
    add_status_history(db, item, status.name)
    item.status = status.name
    db.add(item)
    db.commit()
    return item


def get_item_by_id(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    return item


def list_items(db: Session, status: str = None):
    filters = []
    if status:
        filters = [Item.status == status]
    items = db.query(Item).filter(*filters).all()
    return items
