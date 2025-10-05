import { useEffect, useState } from "react"
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet"
import "leaflet/dist/leaflet.css"

export default function MapView() {
  const [activeLayer, setActiveLayer] = useState("flood")
  const [layerData, setLayerData] = useState(null)

  // Fetch data whenever activeLayer changes
  useEffect(() => {
    fetch(`/api/layers/${activeLayer}`)
      .then((res) => res.json())
      .then((data) => setLayerData(data))
      .catch((err) => console.error("Error loading layer:", err))
  }, [activeLayer])

  // Style functions for each layer
  const styles = {
    flood: (feature) => {
      const colors = { high: "#e53935", medium: "#fb8c00", low: "#43a047" }
      return {
        color: colors[feature.properties.risk_level] || "#1976d2",
        weight: 2,
        fillColor: colors[feature.properties.risk_level] || "#1976d2",
        fillOpacity: 0.35,
      }
    },
    landuse: (feature) => {
      const colors = { high: "#6a1b9a", medium: "#8e24aa", low: "#ce93d8" }
      return {
        color: colors[feature.properties.landuse_level] || "#6a1b9a",
        weight: 2,
        fillColor: colors[feature.properties.landuse_level] || "#6a1b9a",
        fillOpacity: 0.35,
      }
    },
    ndvi: () => ({ color: "#2e7d32", weight: 1, fillColor: "#66bb6a", fillOpacity: 0.4 }),
    lst: () => ({ color: "#ef6c00", weight: 1, fillColor: "#ff9800", fillOpacity: 0.4 }),
    elevation: () => ({ color: "#1565c0", weight: 1, fillColor: "#42a5f5", fillOpacity: 0.4 }),
  }

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      {/* Menu */}
      <div style={{
        position: "absolute", zIndex: 1000, padding: 8,
        background: "white", borderRadius: 4, boxShadow: "0 2px 6px rgba(0,0,0,0.2)"
      }}>
        <label>
          Choose Layer:{" "}
          <select value={activeLayer} onChange={(e) => setActiveLayer(e.target.value)}>
            <option value="flood">Flood Risk</option>
            <option value="landuse">Land Use & Waste</option>
            <option value="ndvi">NDVI</option>
            <option value="lst">LST</option>
            <option value="elevation">Elevation</option>
          </select>
        </label>
      </div>

      {/* Map */}
      <MapContainer center={[4.05, 9.70]} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {layerData && (
          <GeoJSON
            data={layerData}
            style={styles[activeLayer]}
            onEachFeature={(feature, layer) => {
              const props = feature.properties
              layer.bindPopup(
                Object.entries(props)
                  .map(([k, v]) => `<b>${k}</b>: ${v}`)
                  .join("<br/>")
              )
            }}
          />
        )}
      </MapContainer>
    </div>
  )
}
