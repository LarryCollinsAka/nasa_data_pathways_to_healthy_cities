import requests

resp = requests.post(
    "http://127.0.0.1:8000/api/chat/",
    json={"message": "Tell me something fun about Douala"}
)
print(resp.status_code)
print(resp.json())
