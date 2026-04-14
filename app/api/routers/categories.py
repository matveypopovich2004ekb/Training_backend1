from http.client import HTTPException

from fastapi import APIRouter, status
from fastapi import Depends

from app.schemas.categories import CategoryRead, CategoryCreate, CategoryUpdate
from app.api.dependencies import get_category_service
from app.services.categories import CategoryService, CategoryNotFountError


router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
def get_tasks(service: CategoryService = Depends(get_category_service)) -> list[CategoryRead]:
    return service.list_categories()

@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_new_category(
        new_ctgr: CategoryCreate,
        service: CategoryService = Depends(get_category_service)
                        ) -> CategoryRead:
    return service.create_category(payload=new_ctgr)

@router.patch("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def updete_cetegory(category_id: str,
                    update_name: CategoryUpdate,
                    service: CategoryService = Depends(get_category_service)
                    ) -> CategoryRead:
    try:
        return service.update_category(payload=update_name, category_id=category_id)
    except CategoryNotFountError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Категория не найдена"
        )

@router.delete("/{category_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id,
        service: CategoryService = Depends(get_category_service)
                    ) -> None:
    try:
        return service.delete_category(category_id=category_id)
    except CategoryNotFountError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )




