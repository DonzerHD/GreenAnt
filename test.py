from typing import Union
from fastapi import FastAPI
import sqlite3

from pydantic import BaseModel
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

class Action(BaseModel):
    entreprise: str
    prix: int
@app.post("/create_action")
def create_action(action : Action):
    Actions(action.entreprise, action.prix)
    return {"entreprise": action.entreprise, "prix": action.prix}

class OrdreAchat(BaseModel):
    utilisateur_id: int
    action_id: int
    prix_achat: int
    date_achat: str

@app.post("/ordre_d_achat")
def create_ordre_d_achat(ordre: OrdreAchat):
    ordre_d_achat(ordre.utilisateur_id, ordre.action_id, ordre.prix_achat, ordre.date_achat)
    return {"utilisateur_id": ordre.utilisateur_id, "action_id": ordre.action_id, "prix_achat": ordre.prix_achat, "date_achat": ordre.date_achat}