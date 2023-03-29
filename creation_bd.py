import sqlite3

connexion = sqlite3.connect('base.db')
curseur = connexion.cursor()

# Création de la table Utilisateurs
curseur.execute("""CREATE TABLE Utilisateurs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 nom TEXT,
                prenom TEXT,
                email TEXT,
                mdp TEXT)""")

curseur.execute("""CREATE TABLE Associations_suivi_suiveur (
                    suiveur INTEGER,
                    suivi INTEGER,
                    FOREIGN KEY (suivi) REFERENCES Utilisateurs(id),
                    FOREIGN KEY (suiveur) REFERENCES Utilisateurs(id)
                )""")

curseur.execute("""CREATE TABLE Actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    entreprise TEXT,
                    prix INTEGER
                )""")

curseur.execute("""CREATE TABLE Associations_actions_utilisateurs (
                  utilisateur_id INTEGER,
                  action_id INTEGER,
                  prix_achat INTEGER,
                  date_achat TEXT,
                  prix_vente INTEGER,
                  date_vente TEXT,
                  FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id),
                  FOREIGN KEY (action_id) REFERENCES Actions(id)
                )""")


connexion.commit()
connexion.close()

