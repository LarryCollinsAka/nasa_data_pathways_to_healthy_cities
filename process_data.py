# process_data.py (multi-layer export)

import pandas as pd
import json
from shapely.geometry import Point
import geopandas as gpd

# --- Input files ---
NDVI_FILE = "Douala-Points-MOD13Q1-061-results.csv"
DEM_FILE = "Douala-Points-NASADEM-NC-001-results.csv"
LST_FILE = "Douala-Land-use-MOD11A2-061-results.csv"

# --- Outputs ---
OUTPUT_FLOOD = "douala_flood_risk.geojson"
OUTPUT_LANDUSE = "douala_landuse.geojson"

# --- Weights ---
W_ELEVATION = 0.33
W_NDVI = 0.33
W_LST = 0.34

RISK_THRESHOLDS = {
    'high': 0.65,
    'medium': 0.45,
    'low': 0.0
}

# --- Column mappings ---
COLUMN_MAP_DEM = {'NASADEM_NC_001_NASADEM_HGT': 'Elevation_m'}
COLUMN_MAP_NDVI = {'MOD13Q1_061__250m_16_days_NDVI': 'NDVI'}
COLUMN_MAP_LST = {'MOD11A2_061_LST_Day_1km': 'LST_Day_K'}

def normalize(series, reverse=False):
    series = pd.to_numeric(series, errors='coerce')
    series.fillna(series.mean(), inplace=True)
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series))
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if reverse else normalized

def assign_risk_level(score):
    if score >= RISK_THRESHOLDS['high']: return 'high'
    elif score >= RISK_THRESHOLDS['medium']: return 'medium'
    else: return 'low'

def generate_geojson(df, props):
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    features = []
    for _, row in gdf.iterrows():
        feature_props = {k: row[v] for k, v in props.items()}
        features.append({
            "type": "Feature",
            "properties": feature_props,
            "geometry": row['geometry'].__geo_interface__
        })
    return {"type": "FeatureCollection", "features": features}

def main():
    # 1. Load data
    df_ndvi = pd.read_csv(NDVI_FILE)
    df_dem = pd.read_csv(DEM_FILE)
    df_lst = pd.read_csv(LST_FILE)

    # 2. Rename columns
    df_dem.rename(columns=COLUMN_MAP_DEM, inplace=True)
    df_ndvi.rename(columns=COLUMN_MAP_NDVI, inplace=True)
    df_lst.rename(columns=COLUMN_MAP_LST, inplace=True)

    # 3. Merge
    df = df_dem[['ID', 'Latitude', 'Longitude', 'Elevation_m']].copy()
    df['NDVI'] = df_ndvi['NDVI']
    df['LST_Day_K'] = df_lst['LST_Day_K']

    # 4. Flood Risk composite
    df['Norm_Elev_Risk'] = normalize(df['Elevation_m'], reverse=True)
    df['Norm_NDVI_Risk'] = normalize(df['NDVI'], reverse=True)
    df['Norm_LST_Risk'] = normalize(df['LST_Day_K'] / 0.02, reverse=False)

    df['Flood_Risk_Score'] = (
        df['Norm_Elev_Risk'] * W_ELEVATION +
        df['Norm_NDVI_Risk'] * W_NDVI +
        df['Norm_LST_Risk'] * W_LST
    )
    df['risk_level'] = df['Flood_Risk_Score'].apply(assign_risk_level)

    flood_geojson = generate_geojson(df, {
        "city": "ID",
        "risk_level": "risk_level",
        "score": "Flood_Risk_Score"
    })
    with open(OUTPUT_FLOOD, "w") as f:
        json.dump(flood_geojson, f, indent=4)

    # 5. Land Use & Waste Correlation (NDVI + LST only)
    df['LandUse_Waste_Index'] = (
        normalize(df['NDVI'], reverse=True) * 0.5 +
        normalize(df['LST_Day_K'] / 0.02, reverse=False) * 0.5
    )
    df['landuse_level'] = df['LandUse_Waste_Index'].apply(assign_risk_level)

    landuse_geojson = generate_geojson(df, {
        "city": "ID",
        "landuse_level": "landuse_level",
        "index": "LandUse_Waste_Index"
    })
    with open(OUTPUT_LANDUSE, "w") as f:
        json.dump(landuse_geojson, f, indent=4)

    print(f" Flood risk saved to {OUTPUT_FLOOD}")
    print(f" Land use & waste correlation saved to {OUTPUT_LANDUSE}")

if __name__ == "__main__":
    main()
