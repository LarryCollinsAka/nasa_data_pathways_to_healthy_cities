from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import requests, os

router = APIRouter(prefix="/api/chat", tags=["chat"])

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY = os.getenv("NVIDIA_API_KEY")  # set in your environment

SYSTEM_PROMPT = """
You are a respectful, decent, and engaging AI companion.
- When the user asks about maps, risks, or budgets, you can give thoughtful insights.
- When the user just wants to chat, you are light, witty, and friendly — but never offensive.
- Always adapt your tone: serious for analysis, warm and conversational for casual talk.
"""

def call_mistral_chat(user_content: str):
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
        "temperature": 0.6,   # a bit higher for more natural chat
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
    Expects: { "message": "Hello, how are you?" }
    """
    user_message = message.get("message", "")
    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    reply = call_mistral_chat(user_message)
    return JSONResponse(content={"reply": reply})
