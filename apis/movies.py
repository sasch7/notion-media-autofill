import requests
import config

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={config.OMDB_API_KEY}"
    res = requests.get(url)
    return res.json()

