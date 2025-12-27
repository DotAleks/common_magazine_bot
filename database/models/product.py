from typing import Optional

from sqlalchemy import Enum
from sqlalchemy import String, Integer, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

class Product(Base):
    """Product model.
    Attributes:
        id: Primary key
        name: Category name
        counts: 
        sizes: 
        category_id:
    """
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    counts: Mapped[int] = mapped_column(Integer())
    sizes: Mapped[list[str]] = mapped_column(ARRAY(String(5)))
    price: Mapped[int] = mapped_column(Integer())
    image_url: Mapped[str] = mapped_column(String(400))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Optional['Category']] = relationship (back_populates='products')#type: ignore