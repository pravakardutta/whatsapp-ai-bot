from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")

# Webhook verification
@app.get("/webhook")
async def verify_webhook(request: Request):
    challenge = request.query_params.get("hub.challenge")
    token = request.query_params.get("hub.verify_token")

    if token == VERIFY_TOKEN:
        return int(challenge)
    return "Verification failed", 403

# Receive WhatsApp messages
@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    
    # Process incoming messages
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender_id = message["from"]
        text = message["text"]["body"]

        # Generate AI response (We will integrate GPT here)
        response_text = f"Echo: {text}"  # Placeholder response

        send_whatsapp_message(sender_id, response_text)

    return {"status": "received"}

# Function to send a WhatsApp message
def send_whatsapp_message(to, text):
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, json=payload, headers=headers)
