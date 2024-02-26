from fastapi import FastAPI

#create an instance of the FastAPI class
app = FastAPI()

#use the instance to define the path operation
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Path: main.py
import uvicorn
from app import app
