import sqlite3

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()

def Action_all():
    curseur.execute("""SELECT * FROM Actions""")
    return curseur.fetchall()

print(Action_all())

def Action_par_personne(prenom):
    curseur.execute("""SELECT Actions.entreprise, Actions.prix FROM Actions 
                    INNER JOIN Associations_actions_utilisateurs ON Actions.id = Associations_actions_utilisateurs.action_id
                    INNER JOIN Utilisateurs ON Associations_actions_utilisateurs.utilisateur_id = Utilisateurs.id
                    WHERE Utilisateurs.prenom = ?""", (prenom,))
    
    return curseur.fetchall()

print(Action_par_personne("Jean"))

