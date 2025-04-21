from fastapi import Body,FastAPI


app = FastAPI()


BOOKS = [
    {"title":"title one","author":"author one","category":"Science"},
    {"title":"title two","author":"author two","category":"Science"},
    {"title":"title three","author":"author three","category":"history"},
    {"title":"title four","author":"author four","category":"math"},
    {"title":"title five","author":"author five","category":"math"},
    {"title":"title six","author":"author two","category":"math"}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param):
#     return {"dynamic_params": dynamic_param}

@app.get("/books/{book_title}")
async def get_book_by_title(book_title):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return =[]
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return



@app.get("/books/{author}/")
async def get_books_on_author(author:str,category:str):
    book_list=[]
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category').casefold() == category.casefold:
             book_list.append(book)
            
    return book_list


@app.post("/book/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break