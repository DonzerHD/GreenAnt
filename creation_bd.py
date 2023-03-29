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

curseur.execute("""CREATE TABLE Entreprises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    nom TEXT,
                    capital INTEGER
                )""")

curseur.execute("""CREATE TABLE Actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    nom TEXT,
                    valeur INTEGER,
                    utilisateur_id INTEGER,
                    entreprise_id INTEGER,
                    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id),
                    FOREIGN KEY (entreprise_id) REFERENCES Entreprises(id)
                )""")

connexion.commit()
connexion.close()

