from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routers import layers, analysis, chat

app = FastAPI(title="Douala Risk Dashboard API")

# --- CORS (so your React frontend can fetch data) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# include routers
app.include_router(layers.router)
app.include_router(analysis.router)
app.include_router(chat.router)

# serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend/dist")
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not built yet"}