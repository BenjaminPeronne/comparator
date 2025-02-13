import pandas as pd
import psycopg2

# Liste des fichiers Excel à traiter (ajoutez les chemins ici)
file_paths = [
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP CARREFOUR MILENIS NOV 2019.xls",
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP HYPER CASINO ST FRANCOIS NOV 2019.xls",
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP SUPER U SAINTE-ROSE  NOV 2019.xls"
]

# Ensemble pour stocker les familles uniques et éviter les doublons dans l'extraction
families_set = set()

try:
    print("🔄 Début de l'extraction des fichiers Excel...")

    for file_path in file_paths:
        print(f"📂 Traitement du fichier : {file_path}")
        engine = "xlrd" if file_path.endswith(".xls") else "openpyxl"
        # Charger le fichier Excel
        xls = pd.ExcelFile(file_path, engine=engine)

        # Lire la première feuille
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None)

        # Extraire la première colonne contenant les familles de produits
        first_column = df.iloc[:, 0].dropna().astype(str).str.strip()

        # Filtrer les familles de produits (exclure "TOTAL" et "FAMILLE DE PRODUITS")
        file_families = {row for row in first_column if row.isupper() and len(row) > 2 and row not in ["TOTAL", "FAMILLE DE PRODUITS","MONTANT MAXIMUM 180€"]}

        # Ajouter au set global pour éviter les doublons
        families_set.update(file_families)

    # Convertir en DataFrame pour l'insertion
    df_families = pd.DataFrame(sorted(families_set), columns=["label"])

    print("✅ Extraction réussie. Familles de produits détectées :")
    print(df_families)

    # Connexion à PostgreSQL
    print("🔄 Tentative de connexion à PostgreSQL...")

    conn = psycopg2.connect(
        dbname="postgres",      # Nom de la base de données
        user="postgres",        # Nom d'utilisateur PostgreSQL
        password="postgres",    # Mot de passe PostgreSQL
        host="localhost",       # 'localhost' car on se connecte depuis l'hôte (Docker -> Host)
        port="5433"             # Utiliser le port externe 5440 (à adapter si nécessaire)
    )

    cursor = conn.cursor()
    print("✅ Connexion réussie à PostgreSQL.")

    # 1️⃣ SUPPRIMER TOUTES LES DONNÉES AVANT INSERTION
    print("🗑️ Suppression de toutes les entrées existantes dans la table 'categories'...")
    cursor.execute("DELETE FROM categories;")
    conn.commit()  # Valider la suppression

    # 2️⃣ INSÉRER LES NOUVELLES VALEURS
    print("✅ Insertion des nouvelles données...")

    query = "INSERT INTO categories (label) VALUES (%s) ON CONFLICT (label) DO NOTHING"
    cursor.executemany(query, [(label,) for label in df_families["label"]])

    conn.commit()
    
    print("✅ Données insérées avec succès dans PostgreSQL (ancienne table vidée avant).")

except psycopg2.OperationalError as e:
    print(f"❌ Erreur de connexion à PostgreSQL : {str(e)}")

except Exception as e:
    print(f"❌ Erreur inattendue : {str(e)}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
