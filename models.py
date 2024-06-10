
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    status = Column(String(50))
    description = Column(String(50))
    owner_id = Column(Integer)
    owner = relationship("User", back_populates="items")

class ItemHistory(Base):
    __tablename__ = "item_history"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    old_assignee = Column(Integer)
    new_assignee = Column(Integer)