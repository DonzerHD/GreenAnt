import sqlite3
import datetime

# Read:
#  - sectionner les actions disponibles 
def Action_all():
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT * FROM Actions""")
    actions = curseur.fetchall()
    connexion.close()
    return actions

# - obtenir le JWT avec le mail et le MDP

def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM Utilisateurs WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat


# - voir ses actions

def Action_par_personne(id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT Actions.entreprise, Actions.prix FROM Actions 
                    INNER JOIN Associations_actions_utilisateurs ON Actions.id = Associations_actions_utilisateurs.action_id
                    INNER JOIN Utilisateurs ON Associations_actions_utilisateurs.utilisateur_id = Utilisateurs.id
                    WHERE Utilisateurs.id = ?""", (id,))
    actions = curseur.fetchall()
    connexion.close()
    return actions

# - Voir les actions des personnes que l’on suit

def voir_actions_personnes_suivi(suiveur_id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT Actions.entreprise, Actions.prix FROM Actions 
                    INNER JOIN Associations_actions_utilisateurs ON Actions.id = Associations_actions_utilisateurs.action_id
                    INNER JOIN Utilisateurs ON Associations_actions_utilisateurs.utilisateur_id = Utilisateurs.id
                    INNER JOIN Associations_suivi_suiveur ON Utilisateurs.id = Associations_suivi_suiveur.suivi
                    WHERE Associations_suivi_suiveur.suiveur = ?""", (suiveur_id,))
    actions = curseur.fetchall()
    connexion.close()
    return actions


# Obtenir l'id d'un utilisateur depuis son mail et son JWT

def get_id_user_by_email_and_jwt(email:str, jwt:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM Utilisateurs WHERE email=? AND jwt=?
                    """, (email, jwt))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

# Obtenir les infos d'un utilisateur depuis son mail
def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM Utilisateurs WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

# Create: 
# - Créer un utilisateur

def creer_utilisateur(nom, prenom, email, mdp,jwt):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()

    curseur.execute("""INSERT INTO Utilisateurs (nom, prenom, email, mdp, jwt)
                    VALUES (?, ?, ?, ?,?)""", (nom, prenom, email, mdp,jwt))
    id_user = curseur.lastrowid
    connexion.commit()
    connexion.close()
    return id_user

# - Une action

def Actions(entreprise, prix):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Actions (entreprise, prix)
                    VALUES (?, ?)""", (entreprise, prix))
    connexion.commit()
    
# - Une ligne dans le registre

def ordre_d_achat(utilisateur_id, action_id, prix_achat):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Associations_actions_utilisateurs (utilisateur_id, action_id, prix_achat, date_achat)
                    VALUES (?, ?, ?, ? )""", (utilisateur_id, action_id, prix_achat,datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    connexion.commit()
    
# - permet a un utilisateur d’en suivre un autre 

def suivre_utilisateur(email, suiveur_id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    # Récupérer l'identifiant de l'utilisateur correspondant à l'adresse e-mail donnée
    curseur.execute("SELECT id FROM Utilisateurs WHERE email = ?", (email,))
    suivi_id = curseur.fetchone()[0]
    
    # Ajouter une nouvelle ligne dans la table Associations_suivi_suiveur
    curseur.execute("INSERT INTO Associations_suivi_suiveur (suiveur, suivi) VALUES (?, ?)", (suiveur_id, suivi_id))
    
    connexion.commit()

# Update :

# - Changement de mail

def modifier_mail(id:int, nouveau_mail)->None:
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()

    curseur.execute("""
                   UPDATE utilisateurs 
                   SET email = ?
                   WHERE id = ?
                   """, (nouveau_mail, id))
    
    connexion.commit()
    connexion.close()

# Changement de mot de passe

def modifier_mdp(id:int, nouveau_mdp)->None:
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    
    curseur.execute("""
                UPDATE utilisateurs 
                SET mdp = ?
                WHERE id = ?
                """, (nouveau_mdp, id))
    
    connexion.commit()
    connexion.close()

# - Changement de JWT
def update_token(id, token:str)->None:
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE Utilisateurs
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()

# - vendre une action 

def ordre_vente(id , prix_vente):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""UPDATE Associations_actions_utilisateurs SET prix_vente = ?, date_vente = ? WHERE id = ? """, (prix_vente, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") , id))
    connexion.commit()

# Changer la valeur d’une action (fonction prix)

def modifier_valeur_action(id,nouvelle_valeur):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""UPDATE Actions SET valeur = ? WHERE id = ? """, (nouvelle_valeur, id))
    connexion.commit()

# Delete:

# - Supprimer une action

def supprimer_action(id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()

    curseur.execute("""DELETE FROM Actions 
                    WHERE id = ?""", (id,))
    connexion.commit()
    connexion.close()

# - Supprimer un utilisateur 

def supprimer_utilisateur(email):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()

    curseur.execute("""DELETE FROM Utilisateurs 
                    WHERE email = ?""", (email,))
    connexion.commit()
    connexion.close()
    
# - arrêté de suivre

def supprimer_relation(email, suiveur_id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("SELECT id FROM Utilisateurs WHERE email = ?", (email,))
    suivi_id = curseur.fetchone()[0]
    # Supprimer la relation suivi-suiveur correspondante
    curseur.execute("""
                    DELETE FROM Associations_suivi_suiveur 
                    WHERE suivi = ? AND suiveur = ? """,(suivi_id,suiveur_id))
    
    connexion.commit()



# Supprimer une association utilisateurs-actions à partir de son id 
def Association_delete(id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""DELETE FROM Associations_actions_utilisateurs WHERE utilisateur_id = ? """,(id,))
    connexion.commit()
    









