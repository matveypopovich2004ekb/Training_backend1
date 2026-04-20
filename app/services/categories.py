from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryNotFountError(
    Exception
):  # просто чтобы у ошибки было конкретное название
    pass


class CategoryService:
    """Сервис отвечает за всю логику эндпоинтов"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[CategoryRead]:
        result_list = [
            CategoryRead.model_validate(categ) for categ in self.repository.get_all()
        ]
        return result_list

    def create_category(self, payload: CategoryCreate) -> CategoryRead:
        new_categ = self.repository.create(name=payload.name)
        self.db.commit()
        return CategoryRead.model_validate(new_categ)

    def update_category(
        self, payload: CategoryUpdate, category_id: str
    ) -> CategoryRead:
        categ = self.repository.get_by_id(category_id=category_id)
        if categ is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="this category is not found",
            )

        categ.name = payload.name if payload.name is not None else categ.name

        self.db.commit()
        return CategoryRead.model_validate(categ)

    def delete_category(self, category_id: str) -> None:
        categ = self.repository.get_by_id(category_id=category_id)
        if categ is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="this category is not found",
            )

        self.repository.delete(categ)

        self.db.commit()
        return
