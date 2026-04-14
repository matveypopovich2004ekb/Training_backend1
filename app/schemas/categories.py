from pydantic import BaseModel, ConfigDict

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True) #from_attributes=True позволяет взять данные прямо из ORM объекта, да?

    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None