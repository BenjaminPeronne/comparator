import os
import pandas as pd
import psycopg2

# Liste des fichiers Excel à traiter
file_paths = [
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP CARREFOUR MILENIS NOV 2019.xls",
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP HYPER CASINO ST FRANCOIS NOV 2019.xls",
    "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP SUPER U SAINTE-ROSE  NOV 2019.xls"
]

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",  
    port="5433"
)
cursor = conn.cursor()

# Fonction pour extraire le label et la ville depuis le nom de fichier
def extract_store_info(filename):
    base_name = os.path.basename(filename)  # Extraire le nom du fichier sans chemin
    parts = base_name.replace("BQP", "").replace("NOV 2019", "").replace(".xlsx", "").replace(".xls", "").strip().split()

    if len(parts) >= 2:
        label = " ".join(parts[:-1]).strip()
        city = parts[-1].strip()
    else:
        label, city = "UNKNOWN", "UNKNOWN"

    return label, city

# Insérer les magasins dans la table `store`
for file_path in file_paths:
    label, city = extract_store_info(file_path)

    print(f"📌 Extraction du fichier : {file_path}")
    print(f"   🏬 Label : {label}")
    print(f"   📍 Ville : {city}")

    # Assurer que l'adresse, le code postal et le pays ne soient pas NULL
    address = "Adresse inconnue"
    postal_code = "00000"
    country = "France"  # Définir une valeur par défaut

    # Insérer dans PostgreSQL en évitant les doublons
    query = """
    INSERT INTO store (label, address, city, postal_code, country)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (label, city) DO NOTHING;
    """
    cursor.execute(query, (label, address, city, postal_code, country))

# Valider et fermer la connexion
conn.commit()
cursor.close()
conn.close()

print("✅ Insertion terminée dans la base PostgreSQL.")