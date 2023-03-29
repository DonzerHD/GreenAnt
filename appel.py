import sqlite3

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()

def Action_all():
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT * FROM Actions""")
    return curseur.fetchall()

print(Action_all())

def Action_par_personne(id):
    connexion = sqlite3.connect('base.db')
    curseur = connexion.cursor()
    curseur.execute("""SELECT Actions.entreprise, Actions.prix FROM Actions 
                    INNER JOIN Associations_actions_utilisateurs ON Actions.id = Associations_actions_utilisateurs.action_id
                    INNER JOIN Utilisateurs ON Associations_actions_utilisateurs.utilisateur_id = Utilisateurs.id
                    WHERE Utilisateurs.id = ?""", (id,))
    
    return curseur.fetchall()

print(Action_par_personne(1))

# def Association_delete():
#     curseur.execute("""DELETE FROM Associations_actions_utilisateurs WHERE utilisateur_id = 'Jean'""")
#     connexion.commit()
    
# Association_delete()

def ordre_d_achat(utilisateur_id, action_id, prix_achat, date_achat):
      curseur.execute("""INSERT INTO Associations_actions_utilisateurs (utilisateur_id, action_id, prix_achat, date_achat)
                    VALUES (?, ?, ?, ? )""", (utilisateur_id, action_id, prix_achat, date_achat))
      connexion.commit()
      
def ordre_vente(id , prix_vente, date_vente):
      curseur.execute("""UPDATE Associations_actions_utilisateurs SET prix_vente = ?, date_vente = ? WHERE id = ? """, (prix_vente, date_vente , id))
      connexion.commit()
      
ordre_vente(1, 200, "2020-01-01")

def suivre_utilisateur(email, suiveur_id):
    # Récupérer l'identifiant de l'utilisateur correspondant à l'adresse e-mail donnée
    curseur.execute("SELECT id FROM Utilisateurs WHERE email = ?", (email,))
    suivi_id = curseur.fetchone()[0]
    
    # Ajouter une nouvelle ligne dans la table Associations_suivi_suiveur
    curseur.execute("INSERT INTO Associations_suivi_suiveur (suiveur, suivi) VALUES (?, ?)", (suiveur_id, suivi_id))
    
    connexion.commit()
    
# suivre_utilisateur("Laurent@gmail.fr ", 1)
    
def voir_actions_personnes_suivi(suiveur_id):
    curseur.execute("""SELECT Actions.entreprise, Actions.prix FROM Actions 
                    INNER JOIN Associations_actions_utilisateurs ON Actions.id = Associations_actions_utilisateurs.action_id
                    INNER JOIN Utilisateurs ON Associations_actions_utilisateurs.utilisateur_id = Utilisateurs.id
                    INNER JOIN Associations_suivi_suiveur ON Utilisateurs.id = Associations_suivi_suiveur.suivi
                    WHERE Associations_suivi_suiveur.suiveur = ?""", (suiveur_id,))
    
    return curseur.fetchall()

print(voir_actions_personnes_suivi(1))