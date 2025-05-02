import requests
import config

def get_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={config.OMDB_API_KEY}"
    res = requests.get(url)
    return res.json()

def get_movie_images(imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id"
    headers = {
        "Authorization": f"Bearer {config.TMDB_TOKEN}"
    }
    res = requests.get(url, headers=headers)
    data = res.json() 
    backdrop_path = data['movie_results'][0].get('backdrop_path')
    poster_path = data['movie_results'][0].get('poster_path')

    backdrop_url = f"https://image.tmdb.org/t/p/w1280/{backdrop_path}"
    poster_url = f"https://image.tmdb.org/t/p/w1280/{poster_path}"
    return backdrop_url, poster_url