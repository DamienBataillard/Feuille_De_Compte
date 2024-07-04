# Gestion des Dépenses

Une application de gestion des dépenses avec une interface graphique en utilisant Python et Tkinter. Cette application permet de suivre les dépenses mensuelles par catégorie, avec des fonctionnalités pour ajouter des dépenses et visualiser les budgets restants.

## Fonctionnalités

- Ajouter des dépenses avec une description et une catégorie.
- Afficher les dépenses totales et par catégorie.
- Suivre les budgets mensuels par catégorie.
- Interface utilisateur simple et intuitive.

## Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/DamienBataillard/Feuille_De_Compte
    cd nom-du-repo
    ```

2. Créez un environnement virtuel (optionnel mais recommandé) :

    ```bash
    python -m venv venv
    source venv/bin/activate # Pour Linux/Mac
    venv\Scripts\activate # Pour Windows
    ```

3. Installez les dépendances :

    ```bash
    pip install mysql-connector-python python-dotenv
    ```

4. Configurez les variables d'environnement en créant un fichier `.env` dans le répertoire du projet avec le contenu suivant :

    ```plaintext
    DB_HOST=localhost
    DB_NAME=nom_de_votre_base
    DB_USER=votre_utilisateur
    DB_PASSWORD=votre_mot_de_passe
    ```
    Remplacez nom_de_votre_base, votre_utilisateur, et votre_mot_de_passe par les valeurs appropriées pour votre configuration MySQL.
    
## Utilisation

1. Assurez-vous que le serveur MySQL est en cours d'exécution et que la base de données est configurée avec les tables nécessaires :

    ```sql
    CREATE DATABASE nom_de_votre_base;
    USE nom_de_votre_base;

    CREATE TABLE mois (
        id_mois INT AUTO_INCREMENT,
        mois_annee VARCHAR(7),
        PRIMARY KEY(id_mois)
    );

    CREATE TABLE categorie (
        id_categorie INT AUTO_INCREMENT,
        nom_cat VARCHAR(50),
        budget FLOAT,
        PRIMARY KEY(id_categorie)
    );

    CREATE TABLE depense (
        id_depense INT AUTO_INCREMENT,
        montant FLOAT,
        date_depense DATE,
        description VARCHAR(255),
        id_categorie INT NOT NULL,
        id_mois INT NOT NULL,
        PRIMARY KEY(id_depense),
        FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie),
        FOREIGN KEY(id_mois) REFERENCES mois(id_mois)
    );
    ```

2. Exécutez l'application :

    ```bash
    python gestion_depense.py
    ```

## Créer un raccourci sur le bureau (Windows)

1. Créez un fichier batch `lancer_gestion_depenses.bat` avec le contenu suivant :

    ```batch
    @echo off
    cd /d "C:\chemin\vers\votre\projet"
    python gestion_depense.py
    pause
    ```

    Remplacez `C:\chemin\vers\votre\projet` par le chemin réel vers le répertoire de votre projet.

2. Cliquez avec le bouton droit sur le fichier batch `lancer_gestion_depenses.bat` et sélectionnez **Envoyer vers > Bureau (créer un raccourci)**.

3. Pour changer l'icône du raccourci :
    - Téléchargez une icône au format `.ico`.
    - Cliquez avec le bouton droit sur le raccourci sur le bureau et sélectionnez **Propriétés**.
    - Cliquez sur **Changer d'icône...** et sélectionnez l'icône téléchargée.

## Contribuer

Les contributions sont les bienvenues ! Veuillez créer une branche pour vos modifications et ouvrir une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
