from fastapi import FastAPI,Body
from pydantic import BaseModel,Field
from typing import Optional


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
    #id :Optional[int] = None
    id :int | None = None
    title:str = Field(min_length=3)
    author:str= Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=6)

    model_config = {
        "json_schema_extra":{
            "example":[
                {
                    "title":"A Books Title",
                    "author":"Author Name",
                    "description":"A description of the book",
                    "rating":5
                }
            ]
    }
    }


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


@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        

@app.get("/books/")
async def get_books_by_rating(book_rating:int):
    book_list=[]
    for book in BOOKS:
        if book.rating == book_rating:
            book_list.append(book)
            return book_list


@app.post('/create-book')
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    if len(BOOKS) >0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    book_id =1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book")
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
                 


@app.delete("/books/{book_id}")
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if book_id == BOOKS[i].id:
            BOOKS.pop(i)
            return True
        









if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)