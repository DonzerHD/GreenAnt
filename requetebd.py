import sqlite3

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()

def creer_utilisateur(nom, prenom, email, mdp):
    curseur.execute("""INSERT INTO Utilisateurs (nom, prenom, email, mdp)
                    VALUES (?, ?, ?, ?)""", (nom, prenom, email, mdp))
    connexion.commit()
    
def Associations_suivi_suiveur(suiveur, suivi):
    curseur.execute("""INSERT INTO Associations_suivi_suiveur (suiveur, suivi)
                    VALUES (?, ?)""", (suiveur, suivi))
    connexion.commit()

def Actions(entreprise, prix):
    curseur.execute("""INSERT INTO Actions (entreprise, prix)
                    VALUES (?, ?)""", (entreprise, prix))
    connexion.commit()
    
def Asso_actions_utilisateurs(utilisateur_id, action_id, prix_achat, date_achat, prix_vente, date_vente):
    curseur.execute("""INSERT INTO Associations_actions_utilisateurs (utilisateur_id, action_id, prix_achat, date_achat, prix_vente, date_vente)
                    VALUES (?, ?, ?, ?, ?, ?)""", (utilisateur_id, action_id, prix_achat, date_achat, prix_vente, date_vente))
    connexion.commit()
    
# creer_utilisateur("Doe", "John", "Does@gmail.com ", "1234")
# creer_utilisateur("Laurent", "Jean", "Laurent@gmail.fr ", "1234")
# Associations_suivi_suiveur(1, 2)
# Actions("Apple", 100)
# Actions("Google", 200)

#Asso_actions_utilisateurs(1, 1, 100, "2020-01-01" , prix_vente=None, date_vente=None)
# Asso_actions_utilisateurs(2, 2, 200, "2020-01-01" , prix_vente=None, date_vente=None)
    
    
