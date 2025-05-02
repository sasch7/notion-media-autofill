import requests
import config
import cloudscraper

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={config.OMDB_API_KEY}"
    res = requests.get(url)
    return res.json()

def fetch_movie_cover(IMDb_id):
    scraper = cloudscraper.create_scraper()
    url = f"https://api.movieposterdb.com/v1/posters?poster_type_id=2&min_width=1500&min_height=600&imdb={IMDb_id}"
    headers = {
        "Authorization": f"Bearer {config.MPDB_TOKEN}",
        "Accept": "application/json"
    }

    try:
        res = scraper.get(url, headers=headers)
        res.raise_for_status()  # alza errore se status code >= 400
        data = res.json()
        print(data)  # stampa l'intera risposta JSON
        return data
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")
        return None
