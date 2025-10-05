from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests, os

router = APIRouter(prefix="/api/chat", tags=["chat"])

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY = os.getenv("NVIDIA_API_KEY")

# Stronger system prompt
SYSTEM_PROMPT = """
You are the assistant for a Flood Risk Dashboard.
- Always interpret 'city' as the name or code of a geographic area on the map.
- 'risk_level' is one of: low, medium, high — it refers specifically to flood risk.
- 'score' is a numeric flood risk score between 0 and 1, where higher means greater risk.
- When explaining, connect the numbers and categories back to what they mean for people, infrastructure, and planning.
- Never speculate that city codes are scrambled or anonymized — treat them as identifiers for real places.
- If the user asks "What does this mean?" after clicking a polygon, explain the flood risk context clearly and simply.
"""

# Lightweight knowledge base
CITY_KB = {
    "DLACEN": {"name": "Douala-Center", "country": "Cameroon"},
    "DLANRT": {"name": "Douala-North", "country": "Cameroon"},
    "DLAWST": {"name": "Douala-West", "country": "Cameroon"},
    "DLASOU": {"name": "Douala-South", "country": "Cameroon"},
    # add more mappings as needed
}

def call_mistral_chat(user_content: str, context: dict = None):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="NVIDIA_API_KEY not set")

    # Build context text
    context_text = ""
    if context:
        city_code = context.get("city")
        kb_entry = CITY_KB.get(city_code)
        context_text = (
            f"\n\nMap context: City={city_code}, "
            f"Risk={context.get('risk_level')}, "
            f"Score={context.get('score')}."
        )
        if kb_entry:
            context_text += f" This corresponds to {kb_entry['name']} in {kb_entry['country']}."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content + context_text}
        ],
        "max_tokens": 512,
        "temperature": 0.6,
        "top_p": 0.9,
        "stream": False
    }

    resp = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid response from model")

@router.post("/")
def chat_with_model(message: dict):
    """
    Free-form chat endpoint.
    Expects: { "message": "Hello", "context": { "city": "DAKAR", "risk_level": "medium", "score": 0.42 } }
    """
    user_message = message.get("message", "")
    context = message.get("context", {})

    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    reply = call_mistral_chat(user_message, context)
    return JSONResponse(content={"reply": reply})
