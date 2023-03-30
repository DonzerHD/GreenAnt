import sqlite3
import datetime

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()

# Voir toutes les actions
def Action_all():
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT * FROM Actions""")
    actions = curseur.fetchall()
    connexion.close()
    return actions

print(Action_all())


# Voir les actions d'une personne à partir de son id 
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

print(Action_par_personne(1))


# Créer un utilisateur 
def creer_utilisateur(nom, prenom, email, mdp,jwt):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()

    curseur.execute("""INSERT INTO Utilisateurs (nom, prenom, email, mdp, jwt)
                    VALUES (?, ?, ?, ?,?)""", (nom, prenom, email, mdp,jwt))
    id_user = curseur.lastrowid
    connexion.commit()
    connexion.close()
    return id_user
    
# creer_utilisateur('Poppins','Mary','mary@poppins.fr','parapluie')

# Créer une action 

def Actions(entreprise, prix):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Actions (entreprise, prix)
                    VALUES (?, ?)""", (entreprise, prix))
    connexion.commit()

# Actions('Microsoft',3000)
    
# Supprimer un utilisateur à partir de son mail 
def supprimer_utilisateur(email):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()

    curseur.execute("""DELETE FROM Utilisateurs 
                    WHERE email = ?""", (email,))
    connexion.commit()
    connexion.close()

# supprimer_utilisateur('mary@poppins.fr')


# Modifier un utilisateur à partir de son id

def modifier_utilisateur(id:int,nouveau_nom:str,nouveau_prenom, nouveau_mail, nouveau_mdp)->None:
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    
    curseur.execute("""
                   UPDATE utilisateurs 
                   SET nom =  ?, prenom = ?, email = ?, mdp = ?
                   WHERE id = ?
                   """, (nouveau_nom,nouveau_prenom, nouveau_mail, nouveau_mdp, id))
    
    connexion.commit()
    connexion.close()
    
# modifier_utilisateur(1,'poppins','mary','mary@poppins.fr','parapluie')


# Supprimer une association à partir de son id 
def Association_delete(id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""DELETE FROM Associations_actions_utilisateurs WHERE utilisateur_id = ? """,(id,))
    connexion.commit()
    
Association_delete(1)

# Placer un ordre d'achat (== créer une association action-utilisateur)
def ordre_d_achat(utilisateur_id, action_id, prix_achat):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO Associations_actions_utilisateurs (utilisateur_id, action_id, prix_achat, date_achat)
                    VALUES (?, ?, ?, ? )""", (utilisateur_id, action_id, prix_achat,datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    connexion.commit()
    
ordre_d_achat(1,1,30)

# Placer un ordre de vente (== modifier une assocaition action-utilisateur)
def ordre_vente(id , prix_vente):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""UPDATE Associations_actions_utilisateurs SET prix_vente = ?, date_vente = ? WHERE id = ? """, (prix_vente, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") , id))
    connexion.commit()
      
# ordre_vente(1, 200)

# Suivre un utilisateur à partir de son email (== créer une assocaition suivi-suiveur)
def suivre_utilisateur(email, suiveur_id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    # Récupérer l'identifiant de l'utilisateur correspondant à l'adresse e-mail donnée
    curseur.execute("SELECT id FROM Utilisateurs WHERE email = ?", (email,))
    suivi_id = curseur.fetchone()[0]
    
    # Ajouter une nouvelle ligne dans la table Associations_suivi_suiveur
    curseur.execute("INSERT INTO Associations_suivi_suiveur (suiveur, suivi) VALUES (?, ?)", (suiveur_id, suivi_id))
    
    connexion.commit()
    
# suivre_utilisateur("Laurent@gmail.fr ", 1)

# Arrêter de suivre quelqu'un à partir de son email 
def supprimer_relation(email, suiveur_id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("SELECT id FROM Utilisateurs WHERE email = ?", (email,))
    suivi_id = curseur.fetchone()[0]
    # Supprimer la relation suivi-suiveur correspondante
    curseur.execute("""
                    DELETE FROM Associations_suivi_suiveur 
                    WHERE suivi_id = ?,suiveur_id = ? """,(suivi_id,suiveur_id))
    
    connexion.commit()


# Voir les actions des personnes suivies par une personne à partir de son id
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

# print(voir_actions_personnes_suivi(1))

# Authentification 

def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM Utilisateurs WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat


def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM Utilisateurs WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def get_id_user_by_email(email:str):
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM Utilisateurs WHERE email=?
                    """, (email,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

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