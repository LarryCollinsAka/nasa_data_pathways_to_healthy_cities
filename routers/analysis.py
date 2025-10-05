from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests, os

router = APIRouter(prefix="/api/analyze", tags=["analysis"])

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY = os.getenv("NVIDIA_API_KEY")  # set this in your environment

SYSTEM_PROMPT = """
You are an expert urban policy advisor and friendly companion. 
When analyzing polygons or budgets, be precise, structured, and policy‑oriented. 
When chatting casually, be respectful, decent, and light‑hearted — never offensive. 
Always adapt your tone to the user’s intent: serious for analysis, warm and engaging for conversation.
You should produce results or reports in points or tabular format for the following below;
- budget_allocation (percentages across drainage, waste_management, green_infrastructure)
- priority_zones (list of neighborhoods or IDs)
- correlations (short narrative of overlaps or gaps).
"""

def call_mistral(user_content: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct-2503",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.7,
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

@router.post("/{layer}")
def analyze_layer(layer: str, polygon: dict):
    """
    Analyze a clicked polygon from the map.
    Expects polygon properties in the request body.
    """
    props = polygon.get("properties", {})
    if not props:
        raise HTTPException(status_code=400, detail="No polygon properties provided")

    # Craft user prompt
    user_prompt = f"Polygon properties: {props}. Provide budget allocation, priority zones, and correlations."

    analysis = call_mistral(user_prompt)

    # Try to parse JSON if model outputs structured data
    try:
        return JSONResponse(content=json.loads(analysis))
    except Exception:
        # If not valid JSON, just return raw text
        return {"analysis": analysis}
