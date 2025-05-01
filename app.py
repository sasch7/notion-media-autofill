from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Webhook attivo!"

@app.route('/notion-webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("Ricevuto:", data)
    return '', 200
