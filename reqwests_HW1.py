from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class NewBook(BaseModel):
    book_name: str

app = FastAPI()

book = ''

@app.post('/', response_model=str, status_code=status.HTTP_201_CREATED)
def post_newbook(new_book: NewBook):
    global book
    favorite_book = new_book.book_name
    book = favorite_book
    return favorite_book

@app.get('/', response_model=str,  status_code=status.HTTP_200_OK)
def get_favorite_book():
    global book
    return f"Любимая книга на данный момент: {book}"

