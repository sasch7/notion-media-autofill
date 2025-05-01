from flask import Flask, request  
import os  
import logging  

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = ""


app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET']) 
def home():
    return "Webhook attivo!"  

@app.route('/notion-webhook', methods=['POST']) 
def handle_webhook():
    logger.info(f"Headers: {request.headers}")
    
    logger.info(f"Body: {request.get_data(as_text=True)}")
    
    data = request.json
    
    logger.info(f"Ricevuto: {data}")
    
    return '', 200

# Blocco che viene eseguito quando l'app viene avviata
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port)
