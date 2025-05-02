from flask import Flask, request
import os, logging  
import utils, notion_client
import apis.movies as movies

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
    # Get media type
    db_id = data.get("data", {}).get("parent", {}).get("id")
    media_type = utils.get_media_type(db_id)
    logger.info(f"Tipo di media: {media_type}")

    # Get page info
    page_id = data.get("entity", {}).get("id")
    page_data = notion_client.get_page_data(page_id)
    title = page_data['properties']['Title']['title'][0]['plain_text']
    logger.info(f"Title: {title}")

    # Media type handling
    if media_type == "movie":
        movie_data = movies.get_movie_data(title)
        imdb_id = movie_data['imdbID']
        backdrop_url, poster_url = movies.get_movie_images(imdb_id)
        data = movies.set_update_movie_page(movie_data, backdrop_url, poster_url)
        notion_client.update_page(page_id, data)
    elif media_type == "tvseries":
        pass  # Qui aggiungerai la logica per le serie TV
    elif media_type == "book":
        pass  # Qui aggiungerai la logica per i libri
    elif media_type == "game":
        pass  # Qui aggiungerai la logica per i giochi
    elif media_type == "unknown":
        pass  

    # Return (non togliere)
    return '', 200

# Blocco che viene eseguito quando l'app viene avviata
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port)
