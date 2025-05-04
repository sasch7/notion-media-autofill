import requests
import config
import logging

logger = logging.getLogger(__name__)

def search_movie_tmdb(title, year=None, author=None):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": title,
        "year": year,
    }
    headers = {
        "Authorization": f"Bearer {config.TMDB_TOKEN}"
    }
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json()

    if not data['results']:
        logger.warning(f"No TMDB results found for title: {title}")
        return None

    if not author:
        tmdb_id = data['results'][0]['id']
        details = get_movie_details_tmdb(tmdb_id)
        return details

    for result in data['results'][:3]:
        tmdb_id = result['id']
        details = get_movie_details_tmdb(tmdb_id)
        credits = details.get('credits', {})

        director_names = [c['name'].lower() for c in credits.get('crew', []) if c['job'] == 'Director']
        writer_names = [c['name'].lower() for c in credits.get('crew', []) if c['job'] in ['Writer', 'Screenplay']]

        if any(author.lower() in name for name in director_names + writer_names):
            return details

    logger.warning(f"No TMDB results matched author {author} for title: {title}")
    return None

def get_movie_details_tmdb(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {
        "append_to_response": "credits"
    }
    headers = {
        "Authorization": f"Bearer {config.TMDB_TOKEN}"
    }
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    details = res.json()

    backdrop_path = details.get('backdrop_path')
    poster_path = details.get('poster_path')
    details['backdrop_url'] = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None
    details['poster_url'] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    return details

def set_update_movie_page(movie_data, backdrop_url, poster_url):
    backdrop_url = backdrop_url or movie_data.get('backdrop_url')
    poster_url = poster_url or movie_data.get('poster_url')

    country = movie_data['production_countries'][0]['name'] if movie_data.get('production_countries') else 'N/A'
    production = ', '.join([c['name'] for c in movie_data.get('production_companies', [])]) or 'N/A'
    runtime = movie_data.get('runtime')
    language = movie_data['spoken_languages'][0]['name'] if movie_data.get('spoken_languages') else 'N/A'
    imdb_id = movie_data.get('imdb_id', '')
    cast_list = movie_data.get('credits', {}).get('cast', [])
    cast = ', '.join([c['name'] for c in cast_list[:3]]) if cast_list else ''
    release_date = movie_data.get('release_date')
    synopsis = movie_data.get('overview', '')
    directors = ', '.join([c['name'] for c in movie_data.get('credits', {}).get('crew', []) if c['job'] == 'Director'])
    year = release_date.split('-')[0] if release_date else ''
    imdb_rating = str(movie_data.get('vote_average', ''))
    genres = [{"name": g['name']} for g in movie_data.get('genres', [])]
    writers = ', '.join([c['name'] for c in movie_data.get('credits', {}).get('crew', []) if c['job'] in ['Writer', 'Screenplay']])
    title = movie_data.get('title', '')
    imdb_page = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else ''

    data = {
        "properties": {
            "Country": {"select": {"name": country}},
            "Production": {"rich_text": [{"type": "text", "text": {"content": production}}]},
            "Runtime (Minutes)": {"number": runtime},
            "Language": {"select": {"name": language}},
            "IMDb ID": {"rich_text": [{"type": "text", "text": {"content": imdb_id}}]},
            "Cast": {"rich_text": [{"type": "text", "text": {"content": cast}}]},
            "Release Date": {"date": {"start": release_date}} if release_date else None,
            "Poster": {"files": [{"name": "Poster", "external": {"url": poster_url}}]} if poster_url else None,
            "Synopsis": {"rich_text": [{"type": "text", "text": {"content": synopsis}}]},
            "Director(s)": {"rich_text": [{"type": "text", "text": {"content": directors}}]},
            "Year": {"rich_text": [{"type": "text", "text": {"content": year}}]},
            "IMDb Page": {"url": imdb_page} if imdb_page else None,
            "IMDb Rating": {"rich_text": [{"type": "text", "text": {"content": imdb_rating}}]},
            "Genres": {"multi_select": genres},
            "Writer(s)": {"rich_text": [{"type": "text", "text": {"content": writers}}]},
            "Title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "cover": {"type": "external", "external": {"url": backdrop_url}} if backdrop_url else ""
    }

    return data
