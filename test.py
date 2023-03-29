from typing import Union
from fastapi import FastAPI
import sqlite3
from appel import *

app = FastAPI()

@app.get("/actions")
def read_actions_all():
    actions = Action_all()
    return actions

@app.get("/actions/{id}")
def read_actions_par_personne(id: int):
    actions = Action_par_personne(id)
    #return actions
    return {"actions": actions}



