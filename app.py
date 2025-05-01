from flask import Flask, request  
import os  
import logging  
import utils

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
    
    return '', 200

# Blocco che viene eseguito quando l'app viene avviata
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port)
