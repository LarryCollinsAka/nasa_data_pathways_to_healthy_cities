from fastapi import APIRouter
import json
import os

router = APIRouter(prefix="/api/layers", tags=["layers"])

# Path to the generated GeoJSON file in the project root
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "../douala_flood_risk.geojson")

@router.get("/flood")
def get_flood_layer():
    # 1. Attempt to load the actual processed GeoJSON data
    if os.path.exists(GEOJSON_PATH):
        try:
            with open(GEOJSON_PATH, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading GeoJSON: {e}")
            # Fall through to the dummy data on error
            pass

    # 2. Fallback to the original dummy data if the file is missing or corrupted
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"city": "Douala", "risk_level": "high"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[9.65, 4.02], [9.70, 4.02], [9.70, 4.06], [9.65, 4.06], [9.65, 4.02]]]
                },
            }
        ],
    }