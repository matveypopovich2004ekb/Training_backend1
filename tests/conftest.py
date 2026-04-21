from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.categories import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.categories import CategoryService
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


# фикстуры для задач
@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    """Создаём TaskService один раз, чтобы переиспользовать в тестах"""
    task_service = TaskService(db_mock)
    task_service.repository = repository_mock
    return task_service


# фикстуры для категорий
@pytest.fixture
def categroies_repository_mock() -> Mock:
    return Mock(spec=CategoryRepository)


@pytest.fixture
def category_service(
    db_mock: Mock, categroies_repository_mock: Mock
) -> CategoryService:
    service = CategoryService(db_mock)
    service.repository = categroies_repository_mock
    return service
