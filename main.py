from fastapi import FastAPI, HTTPException, Depends

from typing import Optional

from sqlalchemy.orm import Session

from controllers import create_user, create_user_item, get_user_by_email, reassign_item
from database import SessionLocal, engine
from models import Base
from schemas import UserCreate, ItemCreate, User, UserId, Item

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return create_user_item(db=db, item=item, user_id=user_id)


@app.post("/reassign_item/{item_id}/", response_model=Item)
def assign_item(item_id: int, new_owner: UserId, db: Session = Depends(get_db)):
    return reassign_item(db=db, item_id=item_id, new_owner=new_owner)



