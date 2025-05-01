from flask import Flask, request  # Importa Flask e request per gestire le richieste HTTP.
import os  # Modulo per gestire variabili di ambiente, come la porta.
import logging  # Modulo per la gestione dei log.

# Creazione dell'app Flask
app = Flask(__name__)

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Crea un logger per il modulo corrente.

# Definizione route principale (GET "/")
@app.route('/', methods=['GET']) 
def home():
    return "Webhook attivo!"  

# Definizione route per webhook Notion (POST "/notion-webhook")
@app.route('/notion-webhook', methods=['POST']) 
def handle_webhook():
    # Logga le intestazioni della richiesta
    logger.info(f"Headers: {request.headers}")
    
    # Logga il corpo della richiesta
    logger.info(f"Body: {request.get_data(as_text=True)}")
    
    data = request.json
    
    # Logga i dati ricevuti 
    logger.info(f"Ricevuto: {data}")
    
    return '', 200

# Blocco che viene eseguito quando l'app viene avviata
if __name__ == '__main__':
    # Ottiene la porta da una variabile di ambiente, se disponibile (utile per i servizi in produzione).
    # Se la variabile di ambiente non è presente, usa la porta 5000 (valore di default di Flask).
    port = int(os.environ.get("PORT", 5000))
    
    # Avvia il server Flask, in ascolto su tutte le interfacce di rete (host='0.0.0.0'),
    # sulla porta specificata dalla variabile di ambiente o sul valore di default.
    app.run(host='0.0.0.0', port=port)
