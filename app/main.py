from fastapi import HTTPException, FastAPI, Response, Depends
from .database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import ses



app = FastAPI()




@app.get('/')
def initial():
    return {"message": "Successfully initialized the server"}

@app.get('/database')
def success_db(db : Session = Depends(get_db)):
    return {"message": "Successfully connected ti database"}