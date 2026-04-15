from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# это объект конфигурации Alembic,
# который даёт доступ к значениям из используемого .ini файла
from app.core.config import get_settings
config = context.config
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)
# Обрабатываем файл конфигурации для логирования Python.
# Эта строка по сути настраивает логи
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# добавьте сюда объект MetaData вашей модели
# для поддержки 'autogenerate'

from app.models.base import  Base
from app.models.task import TaskORM
from app.models.categories import CategoryORM

target_metadata = Base.metadata

# другие значения из конфигурации, определённые в env.py,
# можно получить так:
# my_important_option = config.get_main_option("my_important_option")
# и т.д.


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    В этом режиме контекст настраивается только с URL,
    без создания Engine, хотя Engine тоже можно использовать.
    Пропуская создание Engine, нам даже не нужен DBAPI.

    Вызовы context.execute() здесь будут просто выводить
    SQL-строки в результат (скрипт).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме.

    В этом случае нам нужно создать Engine
    и связать соединение с контекстом.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()