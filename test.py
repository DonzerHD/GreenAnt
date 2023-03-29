from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    list_a = ["aa", "bb", "cc"]
    return {"item_id": item_id , "item": list_a[item_id-1]}