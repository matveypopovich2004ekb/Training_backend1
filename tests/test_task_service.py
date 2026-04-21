import pytest

from unittest.mock import Mock

from app.models.task import TaskORM
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task import TaskNotFoundError, TaskService


def test_list_tasks_returns_pydantic_models(
    service: TaskService,
    repository_mock: Mock,
) -> None:
    """тест для метода TaskService.list_tasks – должен корректно
    преобразовывать объект БД в Pydantic-модель"""

    # Имитируем, что метод get_all репозитория вернет эти задачи
    repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]

    result = service.list_tasks()

    assert result == [
        TaskRead(id="task-1", title="Изучить pytest", completed=False),
        TaskRead(id="task-2", title="Написать первый тест", completed=True),
    ]


def test_create_task_commits_created_task(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    """тест для TaskService.create_task — должны быть вызваны create репозитория, commit,
    а также TaskORM преобразован в Pydantic-модель"""

    created_task = TaskORM(id="task-1", title="Новая задача", completed=False)
    repository_mock.create.return_value = created_task

    result = service.create_task(TaskCreate(title="Новая задача"))

    repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdate(title="Обновить заголовок"),  # payload
            "Обновить заголовок",  # expected_title
            False,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(completed=True),  # payload
            "Старая задача",  # expected_title
            True,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(title="Готово", completed=True),  # payload
            "Готово",  # expected_title
            True,  # expected_completed
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
    payload: TaskUpdate,
    expected_title: str,
    expected_completed: bool,
) -> None:
    """тест для update_task"""

    task = TaskORM(id="task-1", title="Старая задача", completed=False)
    repository_mock.get_by_id.return_value = task

    result = service.update_task("task-1", payload)

    repository_mock.get_by_id.assert_called_once_with("task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expected_completed,
    }


def test_update_task_raises_when_task_not_found(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    """Tест со сценарием TaskNotFound"""

    repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):  # Должна произойти указанная ошибка
        service.update_task("missing-task", TaskUpdate(title="Неважно"))

    db_mock.commit.assert_not_called()
