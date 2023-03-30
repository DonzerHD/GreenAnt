from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Request, Depends
import sqlite3

from pydantic import BaseModel
from appel import *
from pydantic import BaseModel
import hashlib
from jose import jwt

app = FastAPI()

# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Fonctions utiles :
def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

def decoder_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def verifier_token(req: Request):
    token = req.headers["Authorization"]
    

@app.get("/actions")
def read_actions_all(req:Request):
    try:
        decoder_token(req.headers["Authorization"])
        actions = Action_all()
        return actions
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
        

@app.get("/actions/{id}")
def read_actions_par_personne(id: int):
    actions = Action_par_personne(id)
    #return actions
    return {"actions": actions}

class OrdreAchat(BaseModel):
    utilisateur_id: int
    action_id: int
    prix_achat: int
    date_achat: str
class UserRegister(BaseModel):
    nom:str
    prenom:str
    email:str
    mdp:str

@app.post("/ordre_d_achat")
def create_ordre_d_achat(ordre: OrdreAchat):
    ordre_d_achat(ordre.utilisateur_id, ordre.action_id, ordre.prix_achat, ordre.date_achat)
    return {"utilisateur_id": ordre.utilisateur_id, "action_id": ordre.action_id, "prix_achat": ordre.prix_achat, "date_achat": ordre.date_achat}@app.post("/api/auth/inscription")
async def inscription(user:UserRegister):
    if len(get_users_by_mail(user.email)) > 0:
        raise HTTPException(status_code=403, detail="L'email fourni possède déjà un compte")
    else:
        id_user = creer_utilisateur(user.nom, user.prenom, user.email, hasher_mdp(user.mdp), None)
        token = jwt.encode({
            "email" : user.email,
            "mdp" : user.mdp,
            "id" : id_user
        }, SECRET_KEY, algorithm=ALGORITHM)
        update_token(id_user, token)
        return {"token" : token}
