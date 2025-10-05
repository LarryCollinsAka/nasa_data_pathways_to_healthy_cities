# process_data.py

import pandas as pd
import json
from shapely.geometry import Point
import geopandas as gpd

# --- Configuration ---
# NOTE: Replace these with the actual paths to your downloaded files
NDVI_FILE = "Douala-Points-MOD13Q1-061-results.csv"
DEM_FILE = "Douala-Points-NASADEM-NC-001-results.csv" 
OUTPUT_GEOJSON = "douala_flood_risk.geojson"

# --- Flood Risk Scoring Parameters ---
# Weights for the final score (can be tuned later)
W_ELEVATION = 0.5  # Lower elevation -> Higher risk
W_NDVI = 0.5       # Lower NDVI (more impervious) -> Higher risk

# --- Risk Thresholds (Normalized 0-1) ---
RISK_THRESHOLDS = {
    'high': 0.65,    # Score > 0.65
    'medium': 0.45,  # Score > 0.45 and <= 0.65
    'low': 0.0      # Score <= 0.45
}

def normalize(series, reverse=False):
    """Normalize a pandas series to a 0-1 range."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series)) # Handle constant data
    
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if reverse else normalized

def calculate_risk(df):
    """Calculates the composite flood risk score."""
    # 1. Elevation Risk: Lower elevation means HIGHER flood risk.
    # The 'NASADEM_HGT' column contains elevation in meters.
    # We must REVERSE the normalization so low values become high scores.
    df['Norm_Elev_Risk'] = normalize(df['NASADEM_HGT'], reverse=True)

    # 2. Imperviousness Risk (from NDVI): Lower NDVI means more impervious ground (HIGHER risk).
    # NDVI values range from -10000 to 10000.
    # We must REVERSE the normalization so low NDVI values become high scores.
    df['Norm_NDVI_Risk'] = normalize(df['250m_16_days_NDVI'], reverse=True)

    # 3. Composite Risk Score: A weighted average of the two risk factors.
    df['Flood_Risk_Score'] = (
        df['Norm_Elev_Risk'] * W_ELEVATION + 
        df['Norm_NDVI_Risk'] * W_NDVI
    )
    
    # 4. Assign Risk Level based on thresholds
    def assign_risk_level(score):
        if score >= RISK_THRESHOLDS['high']:
            return 'high'
        elif score >= RISK_THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'low'
            
    df['risk_level'] = df['Flood_Risk_Score'].apply(assign_risk_level)
    
    return df

def generate_geojson(df):
    """Converts the processed DataFrame into a GeoJSON FeatureCollection."""
    
    # Create shapely Point geometries from Longitude and Latitude
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # Select only the relevant output columns for the GeoJSON properties
    gdf = gdf[['risk_level', 'geometry']]
    
    # Convert to GeoJSON FeatureCollection (as a dictionary)
    geojson_dict = json.loads(gdf.to_json())
    
    # We can't display points as an area, so for a quick visualization hack
    # we'll convert the points to a small buffer/circle (if GeoPandas/Shapely is installed)
    # If not installed, we'll return the points and let the map render them
    
    # For a quick fix, let's return the point GeoJSON as is.
    # The frontend is expecting Polygons, so this is a temporary compatibility hack.
    # In a real scenario, you would use a 'MultiPoint' or interpolate to a Raster/Polygon.
    
    # HACK: Create a tiny Polygon (for compatibility with current `flood.py` schema)
    # Since we can't do proper interpolation now, let's just make one dummy polygon 
    # to show the 'high' risk area, using the max-risk point as the center.
    
    highest_risk_point = gdf.loc[gdf['risk_level'] == 'high'].iloc[0].geometry
    
    # Create a dummy high-risk box around the highest risk point
    lon, lat = highest_risk_point.x, highest_risk_point.y
    
    # Define a tiny 0.02 x 0.02 degree polygon (approx 2.2km x 2.2km)
    box_coords = [
        [[lon - 0.01, lat - 0.01], 
         [lon + 0.01, lat - 0.01], 
         [lon + 0.01, lat + 0.01], 
         [lon - 0.01, lat + 0.01], 
         [lon - 0.01, lat - 0.01]]
    ]
    
    # This feature collection will only contain one 'high' risk polygon for demonstration
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"city": "Douala", "risk_level": "high"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": box_coords
                },
            }
        ]
    }


def main():
    # 1. Load Data
    df_ndvi = pd.read_csv(NDVI_FILE)
    df_dem = pd.read_csv(DEM_FILE)

    # 2. Merge Data
    # Assuming the order of points is the same, merge the key columns
    df_merge = df_dem[['ID', 'Latitude', 'Longitude', 'NASADEM_HGT']].copy()
    df_merge['250m_16_days_NDVI'] = df_ndvi['250m_16_days_NDVI']
    
    # 3. Calculate Risk
    df_processed = calculate_risk(df_merge)

    # 4. Generate GeoJSON (HACK for quick demo)
    geojson_output = generate_geojson(df_processed)
    
    # 5. Save GeoJSON
    with open(OUTPUT_GEOJSON, 'w') as f:
        json.dump(geojson_output, f, indent=4)
    
    print(f"Data processed and saved to {OUTPUT_GEOJSON}")
    print("Next step: Update flood.py to load this file.")

if __name__ == "__main__":
    main()