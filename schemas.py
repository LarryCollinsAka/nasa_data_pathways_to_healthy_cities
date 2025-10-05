from typing import List, Dict, Any
from pydantic import BaseModel

class Geometry(BaseModel):
    type: str
    coordinates: List

class Feature(BaseModel):
    type: str = "Feature"
    properties: Dict[str, Any]
    geometry: Geometry

class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]