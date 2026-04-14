from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from uuid import uuid4



the_app = FastAPI()



class Category(BaseModel):
    category_text: str
    id: str #


categories: list[Category] = []

class Create_or_Upd_Category(BaseModel):
    """
        мне кажется не надо создавать отдельный класс
        для того, чтобы обновлять категорию, тк у нас тут всего 1 параметр
        задавется изданчально либо меняется через PUTCH - это текст категории
    """
    category_text: str



@the_app.post('/categories', response_model=Category, status_code=status.HTTP_201_CREATED)
def new_category(user_input_category: Create_or_Upd_Category):
     global categories
     new_cat = Category(id=str(uuid4()), category_text =user_input_category.category_text)
     categories.append(new_cat)
     return new_cat

@the_app.get('/categories', response_model=list[Category], status_code=status.HTTP_200_OK)
def get_category_list():
    global categories
    return categories


@the_app.delete('/categories/{cat_id}', status_code=status.HTTP_204_NO_CONTENT)
def del_category(cat_id: str):
    global categories
    for categ in categories:
        if cat_id == categ.id:
            categories.remove(categ)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Категории сей нету браток, но ты не печалься, а дню прекрасному, да траве зеленой во дворе своем возрадуйся. И маканчика послушай для дзена всеобъемлющего!")

@the_app.patch('/categories/{category_id}', response_model=Category, status_code=status.HTTP_200_OK)
def upd_category(category_id: str, new_text_of_category: Create_or_Upd_Category):
    global categories
    for categ in categories:
        if category_id == categ.id:
            categ.category_text = new_text_of_category.category_text
            return categ

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категории сей нету браток, но ты не печалься, а дню прекрасному, да траве зеленой во дворе своем возрадуйся. И маканчика послушай для дзена всеобъемлющего!")








