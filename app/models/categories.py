from sqlalchemy.orm import mapped_column, Mapped
from app.models.base import Base

class CategoryORM(Base):
    """Модель категории в БД"""
    __tablename__ = "categories"
    
    name: Mapped[str]

