import pandas as pd
import psycopg2

# 🔗 **Connexion PostgreSQL**
def connexion_postgres():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5433"
        )
        print("✅ Connexion réussie à PostgreSQL.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion PostgreSQL : {e}")
        return None

# 📂 **Charger un fichier Excel**
def charger_fichier_excel(chemin_fichier):
    return pd.ExcelFile(chemin_fichier, engine="openpyxl")

# 🔍 **Détecter la ligne contenant les en-têtes**
def trouver_ligne_entete(xls):
    for i in range(5):  # Recherche dans les 5 premières lignes
        temp_df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=i)
        
        # Standardiser les noms des colonnes en majuscules
        temp_df.columns = temp_df.columns.astype(str).str.strip().str.upper()
        
        # Colonnes attendues
        colonnes_recherches = {"FAMILLE DE PRODUITS", "DÉNOMINATION DES PRODUITS", "LIBELLES"}
        
        if any(col in temp_df.columns for col in colonnes_recherches):
            print(f"✅ En-têtes trouvées à la ligne {i + 1}. Colonnes détectées : {temp_df.columns.tolist()}")
            return temp_df
    
    print("❌ Aucune en-tête trouvée. Fichier ignoré.")
    return None

# 📊 **Extraction des produits**
def extraire_donnees_produits(df):
    produits = []
    
    colonne_categorie = df.columns[0]  # Première colonne (Famille de Produits)
    colonne_produit = df.columns[2]  # Troisième colonne (Dénomination des Produits)
    colonne_code_barres = next((col for col in df.columns if "GENCODE" in col), None)  # Dernière colonne "Gencode"
    
    for _, ligne in df.iterrows():
        categorie = str(ligne[colonne_categorie]).strip().upper()
        produit = str(ligne[colonne_produit]).strip()
        barcode = None
        
        if colonne_code_barres and pd.notna(ligne[colonne_code_barres]):
            barcode = str(int(ligne[colonne_code_barres])) if isinstance(ligne[colonne_code_barres], float) else str(ligne[colonne_code_barres])

        # Correction : Remplacer NULL par 'UNKNOWN' pour barcode
        barcode = barcode if barcode else 'UNKNOWN'

        # Correction : Ajouter une date actuelle si NULL
        product_creation_date = pd.Timestamp.now()
        product_modification_date = pd.Timestamp.now()  # Correction ajoutée ici

        if categorie and produit and categorie not in ["TOTAL", "FAMILLE DE PRODUITS"]:
            produits.append((categorie, produit, barcode, product_creation_date, product_modification_date))
    
    return produits

# 🔄 **Traitement des fichiers et insertion dans PostgreSQL**
def traiter_fichiers_et_inserer(conn, chemins_fichiers):
    cursor = conn.cursor()
    tous_produits = []

    for chemin in chemins_fichiers:
        print(f"📂 Traitement du fichier : {chemin}")
        xls = charger_fichier_excel(chemin)
        df = trouver_ligne_entete(xls)
        
        if df is not None:
            produits = extraire_donnees_produits(df)
            tous_produits.extend(produits)

    print("🛒 Insertion des produits dans la table 'products'...")

    for category_label, produit_label, barcode, product_creation_date, product_modification_date in tous_produits:
        try:
            # Vérifier si la catégorie existe, sinon l'insérer
            cursor.execute("SELECT id FROM categories WHERE label = %s", (category_label,))
            category_result = cursor.fetchone()

            if category_result:
                id_category = category_result[0]
            else:
                cursor.execute("INSERT INTO categories (label) VALUES (%s) RETURNING id", (category_label,))
                id_category = cursor.fetchone()[0]
                conn.commit()

            # Insérer le produit sans contrainte de duplication
            cursor.execute("""
                INSERT INTO products (product_label, id_category, barcode, product_creation_date, product_modification_date)
                VALUES (%s, %s, %s, %s, %s);
            """, (produit_label, id_category, barcode, product_creation_date, product_modification_date))

        except psycopg2.Error as e:
            print(f"❌ Erreur SQL : {e}")
            conn.rollback()  # Éviter le blocage des transactions

    conn.commit()
    cursor.close()
    print("✅ Produits insérés avec succès dans PostgreSQL.")

# 🏁 **Exécution principale**
if __name__ == "__main__":
    chemins_fichiers = [
        "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/BQP_CARREFOUR_MILENIS_Nettoye.xlsx",
        "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/BQP_CARREFOUR_FRANCOIS_Nettoye.xlsx",
        "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/BQP_Nettoye_Gencode1.xlsx"
    ]

    print("🔄 Début de l'extraction et de l'insertion des produits...")
    conn = connexion_postgres()

    if conn:
        traiter_fichiers_et_inserer(conn, chemins_fichiers)
        conn.close()
        print("🔌 Connexion PostgreSQL fermée.")
    else:
        print("❌ Impossible de se connecter à la base de données.")