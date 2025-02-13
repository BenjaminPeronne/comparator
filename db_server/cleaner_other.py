import pandas as pd

def nettoyer_fichier_xls(file_path, output_excel):
    """
    Nettoie un fichier Excel (.xls) en dissociant les cellules fusionnées,
    en attribuant la famille de produit à chaque ligne, et en supprimant les lignes vides.
    
    :param file_path: Chemin du fichier Excel (.xls) à nettoyer.
    :param output_excel: Chemin pour enregistrer le fichier nettoyé en .xlsx.
    """
    # Charger le fichier Excel (.xls) avec xlrd
    xls = pd.ExcelFile(file_path, engine="xlrd")

    # Lire la première feuille
    df = pd.read_excel(xls, sheet_name=0, header=None)

    # Trouver la bonne ligne d'en-tête
    header_row = None
    for i in range(5):  # Tester les 5 premières lignes pour détecter les colonnes
        temp_df = pd.read_excel(xls, sheet_name=0, header=i, engine="xlrd")
        if "FAMILLE DE PRODUITS" in temp_df.columns or "DÉNOMINATION DES PRODUITS" in temp_df.columns:
            header_row = i
            df = temp_df
            break

    if header_row is None:
        raise ValueError("❌ Aucune ligne d'en-tête détectée contenant 'FAMILLE DE PRODUITS' ou 'DÉNOMINATION DES PRODUITS'.")

    print(f"✅ En-tête trouvée à la ligne {header_row + 1}. Colonnes détectées : {df.columns.tolist()}")

    # Remplir les cellules vides de la colonne "FAMILLE DE PRODUITS" en utilisant ffill()
    df["FAMILLE DE PRODUITS"] = df["FAMILLE DE PRODUITS"].ffill()

    # Trouver la colonne contenant les produits
    product_column = "LIBELLES" if "LIBELLES" in df.columns else "DÉNOMINATION DES PRODUITS"

    # Supprimer les lignes qui ne contiennent pas de produit (celles où la colonne produit est vide)
    df_cleaned = df.dropna(subset=[product_column])

    # Sauvegarde en .xlsx
    df_cleaned.to_excel(output_excel, index=False, engine="openpyxl")

    print(f"✅ Nettoyage terminé ! Fichier enregistré sous : 📂 {output_excel}")

# Exemple d'utilisation
file_path = "/Users/benjaminperonne/Documents/Developer/University_Developer/M2_S9_MIAGE/Projet/comparator/db_server/src/BQP CARREFOUR MILENIS NOV 2019.xls"  # Remplacez par le vrai chemin du fichier
output_excel = "BQP_CARREFOUR_MILENIS_Nettoye.xlsx"
nettoyer_fichier_xls(file_path, output_excel)
0