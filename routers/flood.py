from fastapi import APIRouter
import json
import os

router = APIRouter(prefix="/api/layers", tags=["layers"])

# Define the path to the newly generated GeoJSON file
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "../douala_flood_risk.geojson")

@router.get("/flood")
def get_flood_layer():
    # Check if the processed data file exists
    if not os.path.exists(GEOJSON_PATH):
        # Fallback to dummy data if the processing script hasn't been run yet
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

    # Load and return the actual processed GeoJSON data
    try:
        with open(GEOJSON_PATH, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return {"error": "Failed to load processed flood data"}, 500