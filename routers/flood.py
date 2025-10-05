from fastapi import APIRouter

router = APIRouter(prefix="/api/layers", tags=["layers"])

@router.get("/flood")
def get_flood_layer():
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