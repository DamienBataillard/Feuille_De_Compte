import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Connexion à la base de données MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

conn = connect_to_db()
if conn:
    cursor = conn.cursor()

    # Création des tables si elles n'existent pas déjà
    cursor.execute('''CREATE TABLE IF NOT EXISTS mois (
                        id_mois INT AUTO_INCREMENT,
                        mois_annee VARCHAR(7),
                        PRIMARY KEY(id_mois)
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS categorie (
                        id_categorie INT AUTO_INCREMENT,
                        nom_cat VARCHAR(50),
                        budget DECIMAL(15,2),
                        PRIMARY KEY(id_categorie)
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS depense (
                        id_depense INT AUTO_INCREMENT,
                        montant DECIMAL(15,2),
                        date_depense DATE,
                        description VARCHAR(255),
                        id_categorie INT NOT NULL,
                        id_mois INT NOT NULL,
                        PRIMARY KEY(id_depense),
                        FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie),
                        FOREIGN KEY(id_mois) REFERENCES mois(id_mois)
                      )''')
    conn.commit()

def get_or_create_current_month():
    mois_actuel = datetime.today().strftime("%Y-%m")
    cursor.execute("SELECT id_mois FROM mois WHERE mois_annee = %s", (mois_actuel,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO mois (mois_annee) VALUES (%s)", (mois_actuel,))
        conn.commit()
        return cursor.lastrowid

def charger_categories():
    categories = {}
    cursor.execute("SELECT id_categorie, nom_cat, budget FROM categorie")
    for row in cursor.fetchall():
        categories[row[1].lower()] = (row[0], row[2])
    return categories

def ajouter_depense():
    try:
        montant = float(entree_montant.get())
    except ValueError:
        messagebox.showerror("Erreur de saisie", "Le montant doit être un nombre valide.")
        return

    categorie = categorie_var.get().lower()
    description = entree_description.get()
    date_depense = datetime.today().date()
    id_mois = get_or_create_current_month()
    
    # Charger les budgets des catégories depuis la base de données
    categories = charger_categories()
    
    if categorie not in categories:
        messagebox.showwarning("Catégorie Invalide", "Cette catégorie n'existe pas.")
        return
    
    id_categorie, budget_categorie = categories[categorie]
    
    # Calculer le budget restant pour la catégorie pour le mois en cours
    cursor.execute("SELECT SUM(montant) FROM depense WHERE id_categorie = %s AND id_mois = %s", (id_categorie, id_mois))
    total_categorie = cursor.fetchone()[0] or 0
    total_categorie += montant
    
    if total_categorie > budget_categorie:
        messagebox.showwarning("Budget Dépassé", f"Vous avez dépassé votre budget pour la catégorie {categorie}!")
        return
    
    # Insertion de la dépense dans la base de données
    cursor.execute("INSERT INTO depense (montant, date_depense, description, id_categorie, id_mois) VALUES (%s, %s, %s, %s, %s)", 
                   (montant, date_depense, description, id_categorie, id_mois))
    conn.commit()
    
    # Mise à jour de l'interface utilisateur
    liste_depenses.insert("", "end", values=(categorie, montant, date_depense, description))
    total_depenses_categories[categorie] = total_categorie
    total_depenses.set(total_depenses.get() + montant)
    budget_restants[categorie].set(budget_categorie - total_categorie)

def charger_depenses():
    # Charger les budgets des catégories depuis la base de données
    categories = charger_categories()
    
    # Chargement des dépenses depuis la base de données pour le mois en cours
    id_mois = get_or_create_current_month()
    cursor.execute("SELECT c.nom_cat, d.montant, d.date_depense, d.description FROM depense d JOIN categorie c ON d.id_categorie = c.id_categorie WHERE d.id_mois = %s", (id_mois,))
    
    for row in cursor.fetchall():
        categorie, montant, date, description = row
        liste_depenses.insert("", "end", values=row)
        total_depenses_categories[categorie] = total_depenses_categories.get(categorie, 0) + montant
        total_depenses.set(total_depenses.get() + montant)
    
    for categorie, (id_categorie, budget) in categories.items():
        budget_restants[categorie].set(budget - total_depenses_categories.get(categorie, 0))

app = tk.Tk()
app.title("Gestion des Dépenses")

# Interface
def validate_float(P):
    if P == "" or P.isdigit() or (P.count('.') == 1 and all(part.isdigit() for part in P.split('.') if part != "")):
        return True
    return False

vcmd = (app.register(validate_float), '%P')

ttk.Label(app, text="Montant:").grid(column=0, row=0, padx=10, pady=5)
entree_montant = ttk.Entry(app, validate="key", validatecommand=vcmd)
entree_montant.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(app, text="Catégorie:").grid(column=0, row=1, padx=10, pady=5)
categorie_var = tk.StringVar()
categorie_menu = ttk.Combobox(app, textvariable=categorie_var)
categorie_menu.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(app, text="Description:").grid(column=0, row=2, padx=10, pady=5)
entree_description = ttk.Entry(app)
entree_description.grid(column=1, row=2, padx=10, pady=5)

ttk.Button(app, text="Ajouter Dépense", command=ajouter_depense).grid(column=0, row=3, columnspan=2, padx=10, pady=10)

liste_depenses = ttk.Treeview(app, columns=("Catégorie", "Montant", "Date", "Description"), show="headings")
liste_depenses.heading("Catégorie", text="Catégorie")
liste_depenses.heading("Montant", text="Montant")
liste_depenses.heading("Date", text="Date")
liste_depenses.heading("Description", text="Description")
liste_depenses.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

total_depenses = tk.DoubleVar(value=0)
total_depenses_categories = {}

# Charger les budgets des catégories
categories = charger_categories()
categorie_menu['values'] = [categorie.capitalize() for categorie in categories]
budget_restants = {categorie: tk.DoubleVar(value=budget) for categorie, (id_categorie, budget) in categories.items()}

ttk.Label(app, text="Total des Dépenses:").grid(column=0, row=5, padx=10, pady=10)
ttk.Label(app, textvariable=total_depenses).grid(column=1, row=5, padx=10, pady=10)

for i, (categorie, (id_categorie, budget)) in enumerate(categories.items(), start=6):
    ttk.Label(app, text=f"Budget Restant {categorie.capitalize()}:").grid(column=0, row=i, padx=10, pady=5)
    ttk.Label(app, textvariable=budget_restants[categorie]).grid(column=1, row=i, padx=10, pady=5)

# Charger les dépenses depuis la base de données au démarrage
charger_depenses()

app.mainloop()

# Fermeture de la connexion à la base de données à la fermeture de l'application
conn.close()
