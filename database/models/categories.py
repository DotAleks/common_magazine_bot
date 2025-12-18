import enum

from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class Gender(enum.Enum):
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
    gender: Mapped[Gender] = mapped_column(Enum(Gender),default=Gender.UNISEX)
