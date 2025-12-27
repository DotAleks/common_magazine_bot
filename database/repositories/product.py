from typing import Optional, Sequence

from sqlalchemy import select

from database.repositories import BaseRepository
from database.models import Product
from database.models.category import Gender


class ProductRepository(BaseRepository):
    async def get_by_id(self, product_id: int) -> Optional[Product]:...
    async def get_by_category_id(self, category_id: int) -> Sequence[Product]:
        """Get product by category"""
        async with self.database.get_session() as session:
            stmt = select(Product).where(Product.category_id == category_id)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def create(self, name: str, counts: int, sizes: list[str], price: int, category_id: int) -> Product:...
    async def delete(self, product_id: int) -> bool:...
    async def update(self, product_id: int, name: Optional[str] = None, counts: Optional[int] = None, sizes: Optional[list[str]] = None, price: Optional[int] = None, category_id: Optional[int] = None) -> ...:...