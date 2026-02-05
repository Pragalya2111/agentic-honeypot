from fastapi import FastAPI, Header, Request
from typing import Optional

app = FastAPI(title="Agentic Honeypot API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
async def run(
    request: Request,
    x_api_key: Optional[str] = Header(default=None)
):
    # Safely read body if it exists
    try:
        body = await request.json()
        user_message = body.get("message")
    except:
        user_message = None

    if not user_message:
        user_message = "Your KYC is pending. Pay ₹10 to verify"

    conversation = [
        user_message,
        "Your account is blocked. Share your UPI ID to unblock.",
        "Send ₹10 to verify and share transaction ID."
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
