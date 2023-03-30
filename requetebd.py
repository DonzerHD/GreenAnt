import sqlite3

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()




def Actions(entreprise, prix):
    curseur.execute("""INSERT INTO Actions (entreprise, prix)
                    VALUES (?, ?)""", (entreprise, prix))
    connexion.commit()
    
def Associations_actions_utilisateurs(utilisateur_id, action_id, prix_achat, date_achat, prix_vente=None, date_vente=None):
    curseur.execute("""INSERT INTO Associations_actions_utilisateurs (utilisateur_id, action_id, prix_achat, date_achat, prix_vente, date_vente)
                    VALUES (?, ?, ?, ?, ?, ?)""", (utilisateur_id, action_id, prix_achat, date_achat, prix_vente, date_vente))
    connexion.commit()

def Associations_suivi_suiveur(suiveur_id, suivi_id):
    curseur.execute("""INSERT INTO Associations_suivi_suiveur (suiveur, suivi)
                    VALUES (?, ?)""", (suiveur_id, suivi_id))
    connexion.commit()

    

    
# creer_utilisateur("Doe", "John", "Does@gmail.com ", "1234")
# creer_utilisateur("Laurent", "Jean", "Laurent@gmail.fr ", "1234")
Associations_suivi_suiveur(1, 2)
Actions("Apple", 100)
Actions("Google", 200)

Associations_actions_utilisateurs(1, 1, 100, "2020-01-01" , prix_vente=None, date_vente=None)
Associations_actions_utilisateurs(2, 2, 200, "2020-01-01" , prix_vente=None, date_vente=None)
    
    
