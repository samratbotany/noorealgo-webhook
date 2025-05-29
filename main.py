from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def fyers_webhook(req: Request):
    data = await req.json()
    print("📥 Webhook received:", data)
    return {"status": "✅ Webhook received", "data": data}

@app.get("/")
async def root():
    return {"message": "Nooré Webhook Server is Alive 🌼"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
