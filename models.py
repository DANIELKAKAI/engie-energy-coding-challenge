import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")
    old_assignees = relationship("ItemHistory", back_populates="old_assignee")
    new_assignees = relationship("ItemHistory", back_populates="new_assignee")


class ItemStatusEnum(enum.Enum):
    NEW = "NEW"
    APPROVED = "APPROVED"
    EOL = "EOL"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    status = Column(Enum(ItemStatusEnum), nullable=False)
    description = Column(String(50))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")
    item_history = relationship("ItemHistory", back_populates="item")


class ItemHistory(Base):
    __tablename__ = "item_history"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="item_history")
    old_assignee_id = Column(Integer, ForeignKey("users.id"))
    old_assignee = relationship("User", back_populates="old_assignees")
    new_assignee_id = Column(Integer, ForeignKey("users.id"))
    new_assignee = relationship("User", back_populates="new_assignees")
