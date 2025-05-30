from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FYERS_ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")  # Stored in Render environment
FYERS_API_URL = "https://api.fyers.in/api/v2/orders"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Nooré Webhook Server is Online 🌸"})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("✅ Received Webhook:", data)

    direction = "CE" if "CE" in data["signal"] else "PE"
    side = 1  # 1 = BUY
    strike = int(data["strike"])
    symbol = f"NSE:BANKNIFTY{strike}{direction}"

    payload = {
        "symbol": symbol,
        "qty": 1,
        "type": 2,
        "side": side,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False
    }

    headers = {
        "Authorization": f"Bearer {FYERS_ACCESS_TOKEN}"
    }

    response = requests.post(FYERS_API_URL, json=payload, headers=headers)
    print("📤 Order Sent. Response:", response.json())

    return jsonify({
        "status": "Executed",
        "symbol": symbol,
        "fyers_response": response.json()
    })
