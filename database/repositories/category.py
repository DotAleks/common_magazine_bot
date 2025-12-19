from typing import Sequence, Optional

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from database.repositories import BaseRepository
from database.models import Category
from database.models.category import Gender

from core.logger import logger


class CategoryRepository(BaseRepository):#TODO: Добавить логирование и протестировать все.
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by id"""
        async with self.database.get_session() as session:
            stmt = select(Category).where(Category.id == category_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        
    async def get_all(self) -> Sequence[Category]:
        """Get all categories"""
        async with self.database.get_session() as session:
            stmt = select(Category)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def get_by_gender(self, gender: Gender) -> Sequence[Category]:
        """Get categories by gender"""
        async with self.database.get_session() as session:
            stmt = select(Category).where(Category.gender == gender)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def create(self, name: str, gender: Gender) -> Category:
        """Create a new category"""
        category = Category(
            name=name,
            gender=gender
        )
        async with self.database.get_session() as session:
            session.add(category)
            await session.flush()
            await session.refresh(category)
            logger.info(f"Category created: id={category.id}, name={category.name}, gender={category.gender}")
            return category
        
    async def update(
        self, 
        category_id: int, 
        name: Optional[str] = None, 
        gender: Optional[Gender] = None
    ) -> Optional[Category]:
        """Update category fields."""
        logger.info(
            f"Updating category {category_id}: "
            f"name={'*' if name else 'None'}, "
            f"gender={'*' if gender else 'None'}"
        )
        if name is None and gender is None:
            logger.debug(f"No changes provided for category {category_id}")
            return await self.get_by_id(category_id)
        
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if gender is not None:
            update_data['gender'] = gender

        async with self.database.get_session() as session:
            stmt = (update(Category)
            .where(Category.id == category_id)
            .values(**update_data)
            .returning(Category))
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
            
    async def delete(self, category_id: int) -> bool:
        """Delete category by ID"""
        async with self.database.get_session() as session:
            category = await self.get_by_id(category_id)

            if not category:
                logger.warning(f"Category {category_id} not found for deletion")
                return False
            
            await session.delete(category)
            logger.info(f"Category {category_id} deleted successfully")
            return True
