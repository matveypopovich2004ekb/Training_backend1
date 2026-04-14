from fastapi import FastAPI, status, HTTPException,Depends
import uvicorn
from uuid import uuid4
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



from contextlib import asynccontextmanager

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker



DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL) # подключение к БД
SessionLocal = sessionmaker(bind=engine) # создание штуки, которая может открывать сессию

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def get_db():
    """Функция для создания сессий с БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(lifespan=lifespan) # lifespan - фуе-яЮ которая выполняется до хзапусска приложеня

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)




# описываем таблицы через класс
class Base(DeclarativeBase):
    """Базовый класс для всех моделей таблиц БД"""
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    """Модель для таблицы задачи в Базе Данных"""
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False) # по умолчанию False

class CategoryORM(Base):
    """Модель для таблицы Категории в Базе Данных"""
    __tablename__ = "categories"
    name: Mapped[str]
#   id заполняется автоматически при создании через Base

# шаблоны для задач Пайдентик
class Task(BaseModel):
    id: str
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str

class  TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


# шаблоны для данных по категориям Пайдентик
class Category(BaseModel):
    name: str
    id: str #

class Create_Category(BaseModel):
    """
        мне кажется не надо создавать отдельный класс
        для того, чтобы обновлять категорию, тк у нас тут всего 1 параметр
        задавется изданчально либо меняется через PUTCH - это текст категории
    """
    name: str

class Update_Category(BaseModel):
    name: str | None = None

# эта функция нужна, чтобы преобразовать данные таблицы в объект Пайдентик
def task_to_model(task: TaskORM) -> Task:
    """Конвертация объекта ORM в Pydantic"""
    return Task(id=task.id, title=task.title, completed=task.completed)

# и эта теперь тоже
def category_to_model(cat: CategoryORM) -> Category:
    return Category(id=cat.id, name=cat.name)


# далее ручки по работе с маршрутом /tasks
@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)) -> list[Task]:
    """Получить список задач"""
    tasks = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks]

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """Создать новую задачу"""
    task = TaskORM(title=payload.title, completed=False)

    db.add(task)
    db.commit()
    return task_to_model(task)

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    """
    Обновить существующую задачу
    task_id получаем из url
    payload получаем из тела запроса
    """
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    task.title = payload.title if payload.title is not None else task.title
    task.completed = payload.completed if payload.completed is not None else task.completed
    db.commit()
    return task_to_model(task)

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Брат задача не найдена брат:( брат")
    db.delete(task)
    db.commit()


# далее ручки по работе с маршрутом /categories
@app.post('/categories', response_model=Category, status_code=status.HTTP_201_CREATED)
def new_category(user_input_category: Create_Category, db: Session = Depends(get_db)) -> Category:
     new_cat = CategoryORM(name = user_input_category.name)
     db.add(new_cat)
     db.commit()
     return category_to_model(new_cat)

@app.get('/categories', response_model=list[Category], status_code=status.HTTP_200_OK)
def get_category_list(db: Session = Depends(get_db)) -> list[Category]:
    category_list = db.scalars(select(CategoryORM)).all() #all() сам переделывает ответ в список объектов CategoryORM
    category_list = [category_to_model(i) for i in category_list]
    return category_list

@app.delete('/categories/{cat_id}', status_code=status.HTTP_204_NO_CONTENT)
def del_category(cat_id: str, db: Session = Depends(get_db)) -> None:
    categ = db.get(CategoryORM, cat_id) #если строка с cat_id найдеься, то она попадет в эту переменную, инача в переменную попоадет None
    if categ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Категории сей нету браток, но ты не печалься, а дню прекрасному, да траве зеленой во дворе своем возрадуйся. И маканчика послушай для дзена всеобъемлющего!")
    db.delete(categ)
    db.commit()
    return

@app.patch('/categories/{category_id}', response_model=Category, status_code=status.HTTP_200_OK)
def upd_category(category_id: str, new_text_of_category: Update_Category, db: Session = Depends(get_db)) -> Category:
    categ = db.get(CategoryORM, category_id)
    if categ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категории сей нету браток, но ты не печалься, а дню прекрасному, да траве зеленой во дворе своем возрадуйся. И маканчика послушай для дзена всеобъемлющего!")
    categ.name = new_text_of_category.name if new_text_of_category.name is not None else  categ.name
    db.commit()
    return category_to_model(categ)

# if __name__ == '__main__':
#     uvicorn.run('main:app', host = '127.0.0.1')





