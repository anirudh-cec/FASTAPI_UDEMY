from fastapi import FastAPI,Depends,HTTPException,Path
import models 
from models import Todos
from database import engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title:str = Field(...,min_length=3)
    description:str= Field(...,min_length=3,max_length=100)
    priority:int = Field(...,gt=0,lt=6)
    completed:bool = Field(default=False)






@app.get("/")
async def read_all(db:db_dependency):
    return db.query(Todos).all()

@app.get("/todos/{todo_id}",status_code =status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int = Path(...,gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")



@app.post("/todos",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request:TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    return todo_model

@app.put("/todos",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_id:int,todo_request:TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.title = todo_request.title
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()
    return todo_model






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)