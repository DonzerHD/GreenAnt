from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Request, Depends
import sqlite3

from pydantic import BaseModel
from appel import *
from pydantic import BaseModel
import hashlib
from jose import JWTError, jwt

app = FastAPI()

# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Fonctions utiles :
def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

def decoder_token(token:str)->dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    # vérifier que le token est valide
    except JWTError:
        raise HTTPException(status_code=401, detail="Le token fourni est invalide ou a expiré")

    
# Read :
# - selectionner les actions disponibles 

@app.get("/actions")
def read_actions_all(req:Request):
    try:
        decoder_token(req.headers["Authorization"])
        actions = Action_all()
        return actions
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
    
# - obtenir le JWT avec le mail et le MDP

class UserLogin(BaseModel):
    email: str
    mdp: str
    
@app.post("/api/auth/login")
async def login(user: UserLogin):
    token = obtenir_jwt_depuis_email_mdp(user.email, hasher_mdp(user.mdp))
    if token is None:
        raise HTTPException(status_code=401, detail="Une erreur s'est produite lors de la génération du token")
    return {"token": token[0]}


# - voir ses actions A FAIRE 

@app.get("/actions/personne")
def read_actions_par_personne(req:Request):
    decode = decoder_token(req.headers["Authorization"])
    id = decode["id"]
    actions = Action_par_personne(id)
    return {"actions": actions}
# - voir les actions des personnes que l’on suit
# - obtenir l'id d'un utilisateur depuis son mail et son JWT

# Create : 
# - Créer un utilisateur

class UserRegister(BaseModel):
    nom:str
    prenom:str
    email:str
    mdp:str
    
@app.post("/api/auth/inscription")
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
# - Une action

class Action(BaseModel):
    entreprise: str
    prix: int
    
@app.post("/create_action")
def create_action(action : Action):
    Actions(action.entreprise, action.prix)
    return {"entreprise": action.entreprise, "prix": action.prix}

# - Une ligne dans le registre

class OrdreAchat(BaseModel):
    utilisateur_id: int
    action_id: int
    prix_achat: int
    


@app.post("/ordre_d_achat")
def create_ordre_d_achat(ordre: OrdreAchat):
    ordre_d_achat(ordre.utilisateur_id, ordre.action_id, ordre.prix_achat)
    return {"utilisateur_id": ordre.utilisateur_id, "action_id": ordre.action_id, "prix_achat": ordre.prix_achat}

# - Permet a un utilisateur d’en suivre un autre 

class Suivi(BaseModel):
    email:str
    
@app.post("/suivre")
async def suivre(suivi:Suivi,req:Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        suiveur_id = decode["id"]
        suivre_utilisateur(suivi.email,suiveur_id)
        return {"La relation suiveur-suivi a bien été créée"}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")


# Update :
# - Changement de mail 
class UpdateEmail(BaseModel):
    email:str
@app.put("/update_email")
async def update_email(update:UpdateEmail,req:Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        id = decode["id"]
        modifier_mail(id,update.email)
        return {"email": update.email}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
# - Changement JWT
class UpdateToken(BaseModel):
    token:str
@app.put("/update_token")
async def update_token_utilisateur(update:UpdateToken,req:Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        id = decode["id"]
        update_token(id,update.token)
        return {"token": update.token}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
# - Changement de mot de passe
class UpdateMdp(BaseModel):
    mdp:str
@app.put("/update_mdp")
async def update_mdp_utilisateur(update:UpdateMdp,req:Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        id = decode["id"]
        modifier_mdp(id,hasher_mdp(update.mdp))
        return {"mdp": update.mdp}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")

# - vendre une action 

class OrdreVente(BaseModel):
    id:int
    prix_vente:int 
    
@app.put("/ordre_de_vente/")
def create_ordre_de_vente(ordre:OrdreVente ,req:Request):
    try:
        decoder_token(req.headers["Authorization"])
        ordre_vente(ordre.id,ordre.prix_vente)
        return {"action_id": ordre.id, "prix_vente":ordre.prix_vente}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
    
# - Changer la valeur d’une action (fonction prix)

# Delete :
# - Supprimer une action

class Action(BaseModel):
    id:int
    
@app.delete("/supprimer_action/")

# - Supprimer un utilisateur 

class User(BaseModel):
    email: str
    mdp: str


@app.delete("/supprimer_utilisateur/")
def supprimer_user(user: User,req:Request):
    try : 
        decoder_token(req.headers["Authorization"])
        token = obtenir_jwt_depuis_email_mdp(user.email, hasher_mdp(user.mdp))
        if token is None:
            raise HTTPException(status_code=401, detail="Une erreur s'est produite lors de la génération du token")
        else :
            supprimer_utilisateur(user.email)
            return {"L'utilisateur a bien été supprimé"}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")

# - arrêté de suivre 

class SupprimerRelation(BaseModel):
    email:str


@app.delete("/stop_relation/")
def stop_relation(supp_relation: SupprimerRelation,req:Request):
    try : 
        decode = decoder_token(req.headers["Authorization"])
        suiveur_id = decode["id"]
        
        # Vérifier si la relation existe avant de la supprimer
        connexion = sqlite3.connect('base.db')
        curseur = connexion.cursor()
        curseur.execute("""
            SELECT id FROM Utilisateurs WHERE email=?
        """, (supp_relation.email,))
        suivi = curseur.fetchone()
        if suivi is None:
            connexion.close()
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        curseur.execute("""
            SELECT suivi FROM Associations_suivi_suiveur WHERE suiveur=? AND suivi=?
        """, (suiveur_id, suivi[0]))
        relation = curseur.fetchone()
        if relation is None:
            connexion.close()
            raise HTTPException(status_code=404, detail="Relation non trouvée")
        
        supprimer_relation(supp_relation.email, suiveur_id)
        connexion.close()
        return {"La relation a bien été supprimée"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Une erreur inattendue s'est produite : ", e)
        raise HTTPException(status_code=500, detail="Une erreur inattendue s'est produite")