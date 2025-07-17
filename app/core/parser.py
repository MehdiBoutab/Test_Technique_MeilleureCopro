import re
import httpx

def extract_bienici_id(url: str) -> str | None:
    """
    Cette fonction extrait l'ID de l'annonce Bienici à partir de l'URL.
    Si l'URL n'est pas valide, elle retourne None.
    """
    if not url:
        return None
    # On cherche un pattern avec l'ID dans l'URL
    match = re.search(r'/annonce/.+/([a-z0-9_\-]+)(\?|$)', url)
    if match:
        return match.group(1)
    return None

async def fetch_bienici_data(bienici_id: str) -> dict | None:
    """
    Cette fonction récupère les infos de l'annonce depuis l'API Bienici.
    Si la requête échoue, on retourne None.
    """
    url_api = f"https://www.bienici.com/realEstateAd.json?id={bienici_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url_api)
            if response.status_code == 200:
                return response.json()
    except httpx.RequestError:
        # Erreur réseau ou autre, on retourne None
        return None
    return None
