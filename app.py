from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Agentic Honeypot API")

class Input(BaseModel):
    message: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(
    payload: Optional[Input] = None,
    x_api_key: Optional[str] = Header(default=None)
):
    user_message = (
        payload.message
        if payload and payload.message
        else "Your KYC is pending. Pay ₹10 to verify"
    )

    conversation = [
        user_message,
        "Your account is blocked. Share your UPI ID to unblock.",
        "Send ₹10 to verify and share transaction ID.",
    ]

    extracted = {
        "upi_ids": [],
        "bank_accounts": [],
        "urls": ["http://fake-bank-verification.com"]
    }

    return {
        "api_key_received": bool(x_api_key),
        "conversation": conversation,
        "extracted": extracted
    }
