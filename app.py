from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import httpx
from entity_extraction import extract_entities

app = FastAPI(title="Agentic Honeypot API")

SCAMMER_URL = "http://127.0.0.1:8000/scammer"
API_KEY = None

class Input(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

def simulated_scammer_reply(message: str) -> str:
    if "kyc" in message.lower():
        return "Your account is blocked. Share your UPI ID to unblock."
    if "upi" in message.lower():
        return "Send ₹10 to verify and share transaction ID."
    return "Urgent action required. Click http://fake-bank-verification.com"


@app.post("/run")
async def run(payload: Input, x_api_key: str = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    conversation = []
    extracted = {"upi_ids": [], "bank_accounts": [], "urls": []}

    scammer_msg = payload.message
    for _ in range(3):
        conversation.append(scammer_msg)
        scammer_msg = simulated_scammer_reply(scammer_msg)
        ents = extract_entities(scammer_msg)
        for k in extracted:
            extracted[k].extend(ents[k])

    return {"conversation": conversation, "extracted": extracted}
