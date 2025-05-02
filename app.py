from flask import Flask, request
import os  
import logging  
import utils
import notion_client
import movies

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
    logger.info(f"Page data: {page_data}")

    # Test MPDB
    test = movies.fetch_movie_cover("tt2294629")
    print
    return '', 200

# Blocco che viene eseguito quando l'app viene avviata
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port)
