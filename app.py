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

async def call_scammer(msg: str):
    async with httpx.AsyncClient() as client:
        r = await client.post(SCAMMER_URL, json={"message": msg})
        return r.json()["reply"]

@app.post("/run")
async def run(payload: Input, x_api_key: str = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    conversation = []
    extracted = {"upi_ids": [], "bank_accounts": [], "urls": []}

    scammer_msg = payload.message
    for _ in range(3):
        conversation.append(scammer_msg)
        scammer_msg = await call_scammer(scammer_msg)
        ents = extract_entities(scammer_msg)
        for k in extracted:
            extracted[k].extend(ents[k])

    return {"conversation": conversation, "extracted": extracted}