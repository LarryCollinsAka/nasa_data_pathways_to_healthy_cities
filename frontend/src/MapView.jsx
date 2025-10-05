import { useEffect, useState } from "react"
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet"
import "leaflet/dist/leaflet.css"   // ✅ ensures Leaflet CSS is bundled

export default function MapView() {
  const [data, setData] = useState(null)
  const [showFlood, setShowFlood] = useState(true)

  // Fetch GeoJSON from backend
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/layers/flood")
        const json = await res.json()
        setData(json)
      } catch (err) {
        console.error("Failed to fetch flood layer:", err)
      }
    }
    fetchData()
  }, [])

  // Style polygons by risk level
  const styleByRisk = (feature) => {
    const risk = feature.properties?.risk_level
    const colors = { high: "#e53935", medium: "#fb8c00", low: "#43a047" }
    return {
      color: colors[risk] || "#1976d2",
      weight: 2,
      fillColor: colors[risk] || "#1976d2",
      fillOpacity: 0.35,
    }
  }

  // Add popup for each feature
  const onEachFeature = (feature, layer) => {
    const city = feature.properties?.city || "Unknown"
    const risk = feature.properties?.risk_level || "N/A"
    layer.bindPopup(`<b>${city}</b><br/>Risk: ${risk}`)
  }

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      {/* Toggle button */}
      <div style={{ position: "absolute", zIndex: 1000, padding: 8 }}>
        <button onClick={() => setShowFlood((s) => !s)}>
          {showFlood ? "Hide Flood Layer" : "Show Flood Layer"}
        </button>
      </div>

      {/* Map */}
      <MapContainer
        center={[4.05, 9.70]} // Douala
        zoom={12}
        style={{ height: "100%", width: "100%", background: "lightgray" }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {showFlood && data && (
          <GeoJSON data={data} style={styleByRisk} onEachFeature={onEachFeature} />
        )}
      </MapContainer>
    </div>
  )
}
