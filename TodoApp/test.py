from fastapi import FastAPI
from typing import Annotated
import models
from models import Todos
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path
from starlette import status
app = FastAPI()

models.Base.metadata.create_all(bind=engine)  ###  this will create dB if it dosent exist

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def get_all(db:db_dependency):
    return db.query(Todos).all()


@app.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo(db:db_dependency,todo_id:int= Path(...,gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Todo Not Found")
   





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)