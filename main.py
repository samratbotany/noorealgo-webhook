from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

FYERS_ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")
FYERS_API_URL = "https://api.fyers.in/api/v2/orders"

@app.get("/")
async def root():
    return {"message": "Nooré Webhook Server is Alive 🌸"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    print("✅ Webhook received:", data)

    direction = "CE" if data.get("signal") == "CE" else "PE"
    side = 1  # Buy
    strike = int(data.get("strike", 0))
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
    print("📤 Order sent. Response:", response.json())

    return {
        "status": "Executed",
        "symbol": symbol,
        "fyers_response": response.json()
    }
