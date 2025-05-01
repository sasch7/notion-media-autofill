from flask import Flask, request
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Webhook attivo!"

@app.route('/notion-webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("Ricevuto:", data)
    return '', 200
