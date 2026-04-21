from unittest.mock import Mock

import pytest

from app.models.categories import CategoryORM
from app.schemas.categories import CategoryRead, CategoryCreate, CategoryUpdate
from app.services.categories import CategoryService, CategoryNotFountError
from categories_HW2 import categories
from tests.conftest import categroies_repository_mock


def test_list_categories_return_pydantic_models(
    category_service: CategoryService,
) -> None:
    """Тест ist_categories на то, что она вернет пайдентик модели и вызовет функциогнал репозитория"""

    category_service.repository.get_all.return_value = [
        CategoryORM(id="1", name="Бытовые"),
        CategoryORM(id="2", name="Работа"),
    ]

    res = category_service.list_categories()
    category_service.repository.get_all.assert_called_once_with()
    assert res == [
        CategoryRead(id="1", name="Бытовые"),
        CategoryRead(id="2", name="Работа"),
    ]


def test_create_category_return_pydantic_model_and_commit(
    category_service: CategoryService, categroies_repository_mock: Mock, db_mock: Mock
) -> None:
    """тест create_category на верный возврат и работу с БД"""

    categroies_repository_mock.create.return_value = CategoryORM(
        id="3", name="New Category"
    )

    res = category_service.create_category(CategoryCreate(name="New Category"))

    categroies_repository_mock.create.assert_called_once_with(name="New Category")
    db_mock.commit.assert_called_once_with()
    assert res == CategoryRead(id="3", name="New Category")


@pytest.mark.parametrize(
    ("payload", "category_found", "expected_answer"),
    [
        pytest.param(
            CategoryUpdate(name="Обновленный заголовок категории"),
            True,
            "Обновленный заголовок категории",
        ),
        pytest.param(CategoryUpdate(), True, "Старый заголовок категории"),
        pytest.param(
            CategoryUpdate(name="Обновленный заголовок категории"),
            False,
            "Ответа быть не должно, тк Ошибка",
        ),
    ],
)
def test_update_category_to_have_no_bug(
    payload: CategoryUpdate,
    category_found: bool,
    expected_answer: str,
    category_service: CategoryService,
    categroies_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    """тест update_category на корректность работы: проверка правильного возврата ПАйдентик моделей
    и падения с ошибкой, если категория не найдена(специально для проверки этого придумано task_found == False)"""

    if category_found == True:  # тестируем случай, когда задача найдена
        category = CategoryORM(id="random id", name="Старый заголовок категории")
        categroies_repository_mock.get_by_id.return_value = category

        res = category_service.update_category(payload=payload, category_id="random id")

        categroies_repository_mock.get_by_id.assert_called_once_with(
            category_id="random id"
        )
        db_mock.commit.assert_called_once_with()
        assert res.model_dump() == {"id": "random id", "name": expected_answer}

    else:  # тестируем случай, если задача не нашлась
        categroies_repository_mock.get_by_id.return_value = None

        with pytest.raises(CategoryNotFountError):
            res = category_service.update_category(
                payload=payload, category_id="random id"
            )

        db_mock.commit.assert_not_called()


@pytest.mark.parametrize(("category_found"), [pytest.param(True), pytest.param(False)])
def test_delete_category_no_bug(
    category_service: CategoryService,
    categroies_repository_mock: Mock,
    db_mock: Mock,
    category_found: bool,
) -> None:
    if category_found == True:
        category = CategoryORM(id="random id", name="Старый заголовок категории")
        categroies_repository_mock.get_by_id.return_value = category

        res = category_service.delete_category(category_id="random id")
        categroies_repository_mock.delete.assert_called_once_with(category)
        db_mock.commit.assert_called_once_with()
        assert res is None

    else:
        categroies_repository_mock.get_by_id.return_value = None
        with pytest.raises(CategoryNotFountError):
            res = category_service.delete_category(category_id="random id")

        db_mock.commit.assert_not_called()
