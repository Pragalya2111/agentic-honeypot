import re

def extract_entities(text: str):
    return {
        "upi_ids": re.findall(r"[\w.-]+@upi", text),
        "bank_accounts": re.findall(r"\b\d{9,18}\b", text),
        "urls": re.findall(r"https?://[^\s]+", text)
    }