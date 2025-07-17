# API MeilleureCopro - Statistiques Immobilières

## Description

Ce projet est une API simple en Python développée avec FastAPI pour fournir des statistiques sur des annonces immobilières issues d’un dataset CSV, et permettre l’ajout d’annonces depuis Bienici.com via leur API JSON.

L’objectif est de calculer les charges de copropriété moyennes et les quantiles (10% et 90%) par département, ville ou code postal. L’API permet aussi d’ajouter une annonce via une URL Bienici.

---

## Fonctionnalités

- Chargement d’un dataset initial d’annonces immobilières.
- Calcul des statistiques sur les charges de copropriété (moyenne, quantiles 10%, 90%) filtrées par zone géographique.
- Ajout d’une annonce immobilière à partir d’une URL Bienici, via leur API JSON.
- Interface web simple pour saisir les filtres et ajouter des annonces.
- API REST documentée avec Swagger (FastAPI).

---

## Installation

1. Cloner ce dépôt :

```bash
git clone <url-du-repo>
cd meilleurecopro
```
2. Créer un environnement virtuel Python (recommandé) :
```
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Installer les dépendances :
```
pip install -r requirements.txt
```

4. Lancement de l’API
```
uvicorn main:app --reload 
```


L’API sera accessible à l’adresse : http://127.0.0.1:8000

## Endpoints principaux

- **GET `/annonces`** : retourne la liste des annonces chargées.
- **POST `/annonces`** : ajoute une annonce via une URL Bienici.
- **GET `/stats`** : retourne les statistiques des charges de copropriété (moyenne, quantiles) selon des filtres (code postal, ville, département).

## Structure du projet

- **`main.py`** : point d’entrée FastAPI.
- **`api.py`** : définition des routes et logique API.
- **`core`**
  - **`data_handler.py`** : classe(s) pour gérer le chargement et la manipulation des données.
  - **`loader.py`** : chargement du dataset initial.
  - **`parser.py`** : fonctions utilitaires pour le parsing et les calculs.
- **`static/`** 
  - **`css`**
    - **`style.css`** : fichiers CSS pour l’interface web.
- **`templates/`** : 
  - **`index.html`**, **`add_annonce.html`** : fichiers HTML pour l’interface utilisateur.
- **`dataset_annonces.csv`** : (local uniquement – à ignorer dans Git).
- **`.gitignore`** : pour exclure le CSV et les fichiers inutiles.
- **`README.md`**


## Tests et validation

Testez les routes avec **Postman**

### Exemple de requête pour obtenir les statistiques :

```http
GET /stats?ville=Paris
```

### Exemple de requête pour ajouter une annonce :
```
POST /annonces
Content-Type: application/json

{
  "url": "https://www.bienici.com/annonce/vente/fontenay-sous-bois/appartement/2pieces/century-21-202_3219_8410?q=%2Frecherche%2Fachat%2Fparis-12e-75012%2Fappartement"
}
