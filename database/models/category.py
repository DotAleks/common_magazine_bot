import enum
from typing import List

from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base


class Gender(enum.Enum):#TODO: перенести в database/enums.py либо core/enums.py
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNISEX = 'UNISEX'

class Category(Base):
    """Product category model.
    Attributes:
        id: Primary key
        name: Category name
        gender: Target gender ('male', 'female', 'unisex')
    """
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70))
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.UNISEX)
    products: Mapped[List['Product']] = relationship(#type: ignore
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='selectin',
        order_by='Product.id'
    )
