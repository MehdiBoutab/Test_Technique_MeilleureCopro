import pandas as pd

def load_dataset(path="dataset_annonces.csv") -> pd.DataFrame:
    """
    Charge le fichier CSV et retourne un DataFrame pandas.
    """
    try:
        data = pd.read_csv(path, sep=",", low_memory=False)
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du dataset : {e}")
        return pd.DataFrame()  # retourne un DataFrame vide si erreur