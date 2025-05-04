import requests
import config
import re
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

def get_movie_data(title, year=None, author=None):
    url = f"http://www.omdbapi.com/?t={title}&apikey={config.OMDB_API_KEY}"
    if year:
        url += f"&y={year}"
    res = requests.get(url)
    data = res.json()

    # Filtro per autore se specificato
    if author and data.get('Director'):
        directors = [d.strip().lower() for d in data['Director'].split(',')]
        if not any(author.lower() in d for d in directors):
            logger.warning(f"Director {author} not found in {directors}")
            return None
        return data

def get_movie_images(imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id"
    headers = {
        "Authorization": f"Bearer {config.TMDB_TOKEN}"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json() 

    if not data.get('movie_results'):
        logger.warning(f"No movie results found for IMDb ID: {imdb_id}")
        return None, None
    
    movie = data['movie_results'][0]
    backdrop_path = movie.get('backdrop_path')
    poster_path = movie.get('poster_path')

    backdrop_url = f"https://image.tmdb.org/t/p/w1280/{backdrop_path}"
    poster_url = f"https://image.tmdb.org/t/p/w1280/{poster_path}"
    return backdrop_url, poster_url

def set_update_movie_page(movie_data, backdrop_url, poster_url):
    country = movie_data.get('Country', 'N/A').split(',')[0].strip()
    production = movie_data.get('Production', 'N/A')
    runtime_raw = movie_data.get('Runtime', 'N/A')
    runtime = int(re.findall(r'\d+', runtime_raw)[0]) if re.findall(r'\d+', runtime_raw) else None
    language = movie_data.get('Language', 'N/A').split(',')[0].strip()
    imdb_id = movie_data.get('imdbID', '')
    cast = movie_data.get('Actors', '')
    release_raw = movie_data.get('Released', '')
    try:
        release_date = datetime.strptime(release_raw, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        release_date = None
    content_rating = movie_data.get('Rated', 'N/A')
    synopsis = movie_data.get('Plot', '')
    directors = movie_data.get('Director', '')
    year = movie_data.get('Year', '')
    imdb_rating = movie_data.get('imdbRating', '')
    genres = [{"name": g.strip()} for g in movie_data.get('Genre', '').split(',')]
    writers = movie_data.get('Writer', '')
    title = movie_data.get('Title', '')
    imdb_page = f"https://www.imdb.com/title/{imdb_id}"

    data = {
        "properties": {
            "Country": {"select": {"name": country}},
            "Production": {"rich_text": [{"type": "text", "text": {"content": production}}]},
            "Runtime (Minutes)": {"number": runtime},
            "Language": {"select": {"name": language}},
            "IMDb ID": {"rich_text": [{"type": "text", "text": {"content": imdb_id}}]},
            "Cast": {"rich_text": [{"type": "text", "text": {"content": cast}}]},
            "Release Date": {"date": {"start": release_date}} if release_date else "",
            "Content Rating": {"select": {"name": content_rating}},
            "Poster": {"files": [{"name": "Poster", "external": {"url": poster_url}}]},
            "Synopsis": {"rich_text": [{"type": "text", "text": {"content": synopsis}}]},
            "Director(s)": {"rich_text": [{"type": "text", "text": {"content": directors}}]},
            "Year": {"rich_text": [{"type": "text", "text": {"content": year}}]},
            "IMDb Page": {"url": imdb_page},
            "IMDb Rating": {"rich_text": [{"type": "text", "text": {"content": imdb_rating}}]},
            "Genres": {"multi_select": genres},
            "Writer(s)": {"rich_text": [{"type": "text", "text": {"content": writers}}]},
            "Title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "cover": {"type": "external", "external": {"url": backdrop_url}}
    }

    return data