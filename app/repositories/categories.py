from app.models.categories import CategoryORM
from sqlalchemy.orm import Session
from sqlalchemy import select


class CategoryRepository():
    """Операции по работе с БД по категориям"""
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        """Получить весь список категорий из БД"""
        categor_list = self.db.scalars(select(CategoryORM)).all()
        return categor_list

    def get_by_id(self, category_id: str) -> CategoryORM:
        """Получить конкретную категорию из БД по id"""
        categ = self.db.get(CategoryORM, category_id)
        return categ


    def create(self, name: str) -> CategoryORM:
        """Добавить категорию, указав ее название"""
        new_categ = CategoryORM(name=name)
        self.db.add(new_categ)
        return new_categ
    
    def delete(self, category) -> None:
        """Удалить категорию"""
        self.db.delete(category)
        return