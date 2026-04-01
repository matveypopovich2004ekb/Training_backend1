from fastapi import FastAPI, status, HTTPException
from uuid import uuid4
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    id: str
    title: str
    completed: bool = False

class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks: list[Task] = []

@app.get('/tasks', response_model=list[Task])
def get_tasks_list():
    global tasks
    return tasks

@app.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def post_task_in_list(name: CreateTask):
    global tasks
    new_task = Task(id=str(uuid4()), title = name.title, completed = False)
    tasks.append(new_task)
    return new_task

@app.patch('/tasks/{task_id}', response_model=Task, status_code=status.HTTP_200_OK)
def putch_task_update(task_id: str, task_update: UpdateTask) -> Task:
    global tasks
    for t in tasks:
        if task_id == t.id:
            if task_update.title is not None:
                t.title = task_update.title
            if task_update.completed is not None:
                t.completed = task_update.completed
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена!")

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Брат задача не найдена брат:( брат")










