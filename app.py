from flask import Flask, request
import os, logging  
import utils, notion_client
import apis.movies as movies
import apis.tvseries as tvseries
import apis.games as games
import apis.books as books

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET']) 
def home():
    return "Webhook attivo!"  

@app.route('/notion-webhook', methods=['POST']) 
def handle_webhook():
    data = request.json
    logger.info(f"Data received: {data}")
    
    db_id = data.get("data", {}).get("parent", {}).get("id")
    media_type = utils.get_media_type(db_id)
    logger.info(f"Tipo di media: {media_type}")

    page_id = data.get("entity", {}).get("id")
    page_data = notion_client.get_page_data(page_id)
    title_raw = page_data.get('properties', {}).get('Title', {}).get('title', [{}])[0].get('plain_text', '')
    title, year, author = utils.parse_title(title_raw)
    logger.info(f"Parsed Title: {title}, Year: {year}, Author: {author}")

    if media_type == "movie":
        movie = movies.search_movie_tmdb(title, year, author)
        if movie:
            backdrop_url, poster_url = movies.get_movie_images_tmdb(movie['id'])
            data = movies.set_update_movie_page(movie, backdrop_url, poster_url)
            notion_client.update_page(page_id, data)
        else:
            notion_client.set_page_title_not_found(page_id, title)

    elif media_type == "tvseries":
        tvseries_data = tvseries.get_tvseries_data(title)
        if not tvseries_data or tvseries_data.get("Response") == "False":
            notion_client.set_page_title_not_found(page_id, title)
        else:
            logger.info(f"{media_type} processing not implemented yet")

    elif media_type == "book":
        book_data = books.get_books_data(title)
        if not book_data or book_data.get("Response") == "False":
            notion_client.set_page_title_not_found(page_id, title)
        else:
            logger.info(f"{media_type} processing not implemented yet")

    elif media_type == "game":
        game_data = games.get_game_data(title)
        if not game_data or game_data.get("Response") == "False":
            notion_client.set_page_title_not_found(page_id, title)
        else:
            logger.info(f"{media_type} processing not implemented yet")

    elif media_type == "unknown":
        logger.info("Media type unknown, skipping...")

    return '', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
