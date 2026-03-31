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

class CreateBook(BaseModel):
    book_name: str

favorite_book = ''

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


for route in app.routes:
    print(route.path, route.methods)






