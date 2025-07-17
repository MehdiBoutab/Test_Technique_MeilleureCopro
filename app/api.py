from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from core.parser import extract_bienici_id, fetch_bienici_data
from core.data_handler import df_initial, df_annonces
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    # Page d'accueil avec formulaire pour faire des stats
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def home_post(request: Request, filtre: str = Form(...), valeur: str = Form(...)):
    global df_annonces, df_initial
    # On combine les données initiales avec celles ajoutées par les utilisateurs
    df_combined = pd.concat([df_initial, df_annonces], ignore_index=True)

    filtre = filtre.upper()
    valeur = valeur.strip().lower()

    # Vérifie que le filtre est valide
    if filtre not in ["DEPT_CODE", "CITY", "ZIP_CODE"]:
        erreur = "Filtre invalide."
        return templates.TemplateResponse("index.html", {"request": request, "erreur": erreur})

    # Filtrer les annonces selon la valeur
    df_filtered = df_combined[df_combined[filtre].str.lower() == valeur]

    # Si rien trouvé, on affiche un message d'erreur
    if df_filtered.empty:
        erreur = f"Aucune donnée trouvée pour {filtre} = '{valeur}'."
        return templates.TemplateResponse("index.html", {"request": request, "erreur": erreur})

    # Calcul des stats
    moyenne = df_filtered["CONDOMINIUM_EXPENSES"].mean()
    quantile_10 = df_filtered["CONDOMINIUM_EXPENSES"].quantile(0.1)
    quantile_90 = df_filtered["CONDOMINIUM_EXPENSES"].quantile(0.9)

    resultats = {
        "moyenne": round(moyenne, 2),
        "quantile_10": round(quantile_10, 2),
        "quantile_90": round(quantile_90, 2)
    }

    # Affiche la page avec les résultats
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "resultats": resultats,
            "filtre": filtre,
            "valeur": valeur,
        }
    )

@router.get("/add-annonce", response_class=HTMLResponse)
async def form_add_annonce(request: Request):
    # Page formulaire pour ajouter une annonce via URL Bienici
    return templates.TemplateResponse("add_annonce.html", {"request": request})

@router.post("/add-annonce", response_class=HTMLResponse)
async def add_annonce(request: Request, url_annonce: str = Form(...)):
    global df_annonces, df_initial

    erreur = None
    message = None

    # Extraction de l'ID Bienici depuis l'URL donnée
    bienici_id = extract_bienici_id(url_annonce)
    if not bienici_id:
        erreur = "URL invalide ou ID Bienici non trouvé."
        return templates.TemplateResponse("add_annonce.html", {"request": request, "erreur": erreur})

    # Appel à l'API Bienici pour récupérer les données
    data = await fetch_bienici_data(bienici_id)
    if not data:
        erreur = "Impossible de récupérer les données depuis Bienici."
        return templates.TemplateResponse("add_annonce.html", {"request": request, "erreur": erreur})

    ad_id = data.get("id")

    # Vérifie si l'annonce existe déjà dans les datasets
    if ad_id in df_initial["ID"].values or ad_id in df_annonces["ID"].values:
        erreur = "Cette annonce a déjà été ajoutée."
        return templates.TemplateResponse("add_annonce.html", {"request": request, "erreur": erreur})

    # Récupération des infos importantes
    condo_expenses = data.get("annualCondominiumFees")
    city = data.get("city") or data.get("district", {}).get("name")
    postal_code = data.get("postalCode") or data.get("district", {}).get("postal_code")
    dept_code = data.get("departmentCode") or data.get("district", {}).get("cp")

    if condo_expenses is None or city is None:
        erreur = "Les données reçues sont incomplètes pour cette annonce."
        return templates.TemplateResponse("add_annonce.html", {"request": request, "erreur": erreur})

    # Préparation de la nouvelle annonce
    new_annonce = {
        "ID": ad_id,
        "CITY": city,
        "ZIP_CODE": postal_code,
        "DEPT_CODE": dept_code,
        "CONDOMINIUM_EXPENSES": condo_expenses
    }

    # Ajoute la nouvelle annonce dans le dataframe en mémoire
    df_annonces = pd.concat([df_annonces, pd.DataFrame([new_annonce])], ignore_index=True)

    message = f"Annonce ajoutée avec succès pour la ville {city}."
    return templates.TemplateResponse("add_annonce.html", {"request": request, "message": message})

@router.get("/annonces")
async def get_annonces():
    global df_annonces
    # Retourne toutes les annonces ajoutées en JSON
    return JSONResponse(content=df_annonces.to_dict(orient="records"))
