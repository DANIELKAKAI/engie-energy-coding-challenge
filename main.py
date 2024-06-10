from fastapi import FastAPI, HTTPException, Depends

from typing import Optional, List

from sqlalchemy.orm import Session

from controllers import (
    create_user,
    create_user_item,
    get_user_by_email,
    reassign_item,
    change_item_status,
    list_items,
    get_item_by_id,
)
from database import SessionLocal, engine
from models import Base
from schemas import (
    UserCreate,
    ItemCreate,
    User,
    UserId,
    Item,
    Status,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "Azure"}


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_by_id(db=db, item_id=item_id)


@app.get("/items/", response_model=List[Item])
def read_items(status: Optional[str] = None, db: Session = Depends(get_db)):
    return list_items(db=db, status=status)


@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return create_user_item(db=db, item=item, user_id=user_id)


@app.post("/reassign_item/{item_id}/", response_model=Item)
def assign_item(
    item_id: int, new_owner: UserId, db: Session = Depends(get_db)
):
    return reassign_item(db=db, item_id=item_id, new_owner=new_owner)


@app.post("/item/status/{item_id}/", response_model=Item)
def assign_item(item_id: int, status: Status, db: Session = Depends(get_db)):
    return change_item_status(db=db, item_id=item_id, status=status)
