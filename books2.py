from fastapi import FastAPI,Body
from pydantic import BaseModel,Field


app = FastAPI()

class Book():
    id:int
    title:str
    author:str
    description:str
    rating:int


    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id :int = Field(int)
    title:str = Field(min_length=3)
    author:str= Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=6)


BOOKS=[
    Book(1,"computer Science","Ande","Best Computer science Book",5),
    Book(2,"AI","Anirudh","Best Book on AI",5),
    Book(3,"Data Science","CG","Must have if you want to learn DS",4),
    Book(4,"Coding with Python","Anirudh","Must have if you want to learn Python",3),
    Book(5,"Coding with Java","Head First","Must have if you want to learn Java",3),
    Book(6,"GO Lang","CG","Must have if you want to learn GO",5)

]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post('/create-book')
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(new_book)