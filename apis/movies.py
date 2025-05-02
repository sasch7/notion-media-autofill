import requests
import config
import cloudscraper
import logging

logger = logging.getLogger(__name__)

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={config.OMDB_API_KEY}"
    res = requests.get(url)
    return res.json()

def fetch_movie_cover(IMDb_id):
    scraper = cloudscraper.create_scraper()
    url = f"https://api.movieposterdb.com/v1/posters?poster_type_id=2&min_width=1500&min_height=600&imdb={IMDb_id}"
    headers = {
        "Authorization": f"Bearer {config.MPDB_TOKEN}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        res = scraper.get(url, headers=headers)
        logger.info(f"HTTP status: {res.status_code}")
        logger.info(f"Raw response: {res.text}")
        res.raise_for_status()
        data = res.json()
        logger.info(f"Parsed JSON: {data}")
        return data
    except Exception as e:
        logger.error(f"Errore durante la richiesta a MoviePosterDB: {e}")
        return None