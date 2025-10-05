from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json, os

router = APIRouter(prefix="/api/layers", tags=["layers"])

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_geojson(filename: str, fallback: dict) -> dict:
    """Utility to load a GeoJSON file or return fallback if missing/corrupt."""
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return fallback

# --- Flood Risk Layer ---
@router.get("/flood")
def get_flood_layer():
    return JSONResponse(content=load_geojson(
        "douala_flood_risk.geojson",
        {"type": "FeatureCollection", "features": []}
    ))

# --- Land Use & Waste Correlation Layer ---
@router.get("/landuse")
def get_landuse_layer():
    return JSONResponse(content=load_geojson(
        "douala_landuse.geojson",
        {"type": "FeatureCollection", "features": []}
    ))

# --- Optional: NDVI Layer ---
@router.get("/ndvi")
def get_ndvi_layer():
    return JSONResponse(content=load_geojson(
        "douala_ndvi.geojson",
        {"type": "FeatureCollection", "features": []}
    ))

# --- Optional: LST Layer ---
@router.get("/lst")
def get_lst_layer():
    return JSONResponse(content=load_geojson(
        "douala_lst.geojson",
        {"type": "FeatureCollection", "features": []}
    ))

# --- Optional: Elevation Layer ---
@router.get("/elevation")
def get_elevation_layer():
    return JSONResponse(content=load_geojson(
        "douala_elevation.geojson",
        {"type": "FeatureCollection", "features": []}
    ))
