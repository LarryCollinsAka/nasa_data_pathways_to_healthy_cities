# process_data.py

import pandas as pd
import json
from shapely.geometry import Point
import geopandas as gpd
import os

# --- Configuration (Ensure these file names match your downloaded files) ---
NDVI_FILE = "Douala-Points-MOD13Q1-061-results.csv"
DEM_FILE = "Douala-Points-NASADEM-NC-001-results.csv" 
OUTPUT_GEOJSON = "douala_flood_risk.geojson"

# --- Flood Risk Scoring Parameters ---
W_ELEVATION = 0.5
W_NDVI = 0.5

# Risk Thresholds (Normalized 0-1)
RISK_THRESHOLDS = {
    'high': 0.65,
    'medium': 0.45,
    'low': 0.0
}

# --- Mapping for Renaming Columns ---
# These are the exact headers from your uploaded CSVs, mapped to simple names.
COLUMN_MAP_DEM = {
    'NASADEM_NC_001_NASADEM_HGT': 'Elevation_m'
}
COLUMN_MAP_NDVI = {
    'MOD13Q1_061__250m_16_days_NDVI': 'NDVI'
}

def normalize(series, reverse=False):
    """Normalize a pandas series to a 0-1 range."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series)) 
    
    # We must ensure data is numeric before normalization
    series = pd.to_numeric(series, errors='coerce').fillna(series.mean())
    
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if reverse else normalized

def calculate_risk(df):
    """Calculates the composite flood risk score."""
    
    # 1. Elevation Risk: Lower elevation means HIGHER flood risk. REVERSE normalization.
    df['Norm_Elev_Risk'] = normalize(df['Elevation_m'], reverse=True)

    # 2. Imperviousness Risk (from NDVI): Lower NDVI means more impervious ground (HIGHER risk). REVERSE normalization.
    df['Norm_NDVI_Risk'] = normalize(df['NDVI'], reverse=True)

    # 3. Composite Risk Score
    df['Flood_Risk_Score'] = (
        df['Norm_Elev_Risk'] * W_ELEVATION + 
        df['Norm_NDVI_Risk'] * W_NDVI
    )
    
    # 4. Assign Risk Level
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
    """Converts the highest risk point into a temporary polygon for visualization."""
    
    # Create GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # Find the highest risk point
    highest_risk_gdf = gdf.loc[gdf['Flood_Risk_Score'] == gdf['Flood_Risk_Score'].max()]
    if highest_risk_gdf.empty:
        return {"type": "FeatureCollection", "features": []}

    highest_risk_point = highest_risk_gdf.iloc[0].geometry
    lon, lat = highest_risk_point.x, highest_risk_point.y
    risk_level = highest_risk_gdf.iloc[0]['risk_level']
    
    # HACK: Create a temporary Polygon (0.03 x 0.03 degrees) around the highest risk point
    box_coords = [
        [[lon - 0.015, lat - 0.015], 
         [lon + 0.015, lat - 0.015], 
         [lon + 0.015, lat + 0.015], 
         [lon - 0.015, lat + 0.015], 
         [lon - 0.015, lat - 0.015]]
    ]
    
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"city": "Douala", "risk_level": risk_level},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": box_coords
                },
            }
        ]
    }

def main():
    try:
        # --- 1. Load Data ---
        # NOTE: Removed skiprows=1 because the header is on the first line.
        df_ndvi = pd.read_csv(NDVI_FILE)
        df_dem = pd.read_csv(DEM_FILE)

        # --- 2. Rename and Merge Data ---
        df_dem.rename(columns=COLUMN_MAP_DEM, inplace=True)
        df_ndvi.rename(columns=COLUMN_MAP_NDVI, inplace=True)
        
        # Merge key geometry/ID columns from DEM, then add the NDVI value
        # Ensure all columns needed are present
        required_cols = ['ID', 'Latitude', 'Longitude', 'Elevation_m']
        if not all(col in df_dem.columns for col in required_cols):
             raise KeyError(f"Missing required columns in DEM file after rename. Expected: {required_cols}. Got: {list(df_dem.columns)}")

        if 'NDVI' not in df_ndvi.columns:
             raise KeyError(f"Missing 'NDVI' column in NDVI file after rename. Got: {list(df_ndvi.columns)}")
        
        df_merge = df_dem[['ID', 'Latitude', 'Longitude', 'Elevation_m']].copy()
        df_merge['NDVI'] = df_ndvi['NDVI']
        
        # --- 3. Calculate Risk ---
        df_processed = calculate_risk(df_merge)

        # --- 4. Generate and Save GeoJSON ---
        geojson_output = generate_geojson(df_processed)
        
        with open(OUTPUT_GEOJSON, 'w') as f:
            json.dump(geojson_output, f, indent=4)
        
        print(f"✅ Success! Data processed and saved to {OUTPUT_GEOJSON}")
        print("NEXT STEP: Ensure your flood.py is updated, then run FastAPI.")

    except FileNotFoundError:
        print(f" ERROR: One or both input files not found. Check names and location.")
    except KeyError as e:
        print(f" ERROR: Column renaming failed. {e}")
    except Exception as e:
        print(f" UNEXPECTED ERROR during processing: {e}")

if __name__ == "__main__":
    # Ensure pandas, shapely, and geopandas are installed:
    # pip install pandas shapely geopandas
    main()