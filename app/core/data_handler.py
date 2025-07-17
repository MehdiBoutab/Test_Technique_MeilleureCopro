import pandas as pd
from core.loader import load_dataset

# On charge les données initiales au lancement du module
df_initial = load_dataset()

# DataFrame vide pour stocker les annonces ajoutées à chaud
df_annonces = pd.DataFrame(columns=["ID", "CITY", "ZIP_CODE", "DEPT_CODE", "CONDOMINIUM_EXPENSES"])

def get_condo_expenses(data: dict) -> float | None:
    """
    Essaie de récupérer les charges de copropriété sur différentes clés possibles.
    Retourne la valeur si trouvée, sinon None.
    """
    keys_to_check = ["annualCondominiumFees", "charges", "charges_copro", "monthlyCharges"]
    for key in keys_to_check:
        if key in data:
            return data[key]
    return None

def annonce_exists(ad_id: str) -> bool:
    """
    Vérifie si l'annonce avec cet ID existe déjà dans les données initiales ou ajoutées.
    """
    global df_initial, df_annonces
    return ad_id in df_initial["ID"].values or ad_id in df_annonces["ID"].values

def add_annonce(data: dict) -> bool:
    """
    Ajoute une annonce dans df_annonces si elle n'existe pas déjà et si les infos clés sont présentes.
    Retourne True si l'ajout a réussi, sinon False.
    """
    global df_annonces

    ad_id = data.get("id")
    if not ad_id:
        return False

    if annonce_exists(ad_id):
        return False

    condo_expenses = get_condo_expenses(data)
    city = data.get("city") or data.get("district", {}).get("name")
    postal_code = data.get("postalCode") or data.get("district", {}).get("postal_code")
    dept_code = data.get("departmentCode") or data.get("district", {}).get("cp")

    if condo_expenses is None or city is None:
        return False

    new_annonce = {
        "ID": ad_id,
        "CITY": city,
        "ZIP_CODE": postal_code,
        "DEPT_CODE": dept_code,
        "CONDOMINIUM_EXPENSES": condo_expenses
    }

    # On concatène la nouvelle annonce au DataFrame des annonces ajoutées
    df_annonces = pd.concat([df_annonces, pd.DataFrame([new_annonce])], ignore_index=True)
    return True
