import React, { useState } from "react";
import MapView from "./MapView";  
import ChatBox from "./ChatBox";

function App() {
  const [showChat, setShowChat] = useState(true);
  const [polygonContext, setPolygonContext] = useState(null);

  // Example: MapView calls this when a polygon is clicked
  const handlePolygonClick = (context) => {
    setPolygonContext(context);
    setShowChat(true); // auto-open chat when a polygon is clicked
  };

  return (
    <div style={{ display: "flex", height: "100vh", position: "relative" }}>
      {/* Map always visible */}
      <div style={{ flex: showChat ? 3 : 1, transition: "flex 0.3s ease" }}>
        <MapView onPolygonClick={handlePolygonClick} />
      </div>

      {/* Chat panel (collapsible) */}
      {showChat && (
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            borderLeft: "1px solid #ccc",
            background: "#fff",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "0.5rem",
              borderBottom: "1px solid #ccc",
              background: "#f5f5f5",
            }}
          >
            <h2 style={{ margin: 0 }}>Assistant Chat</h2>
            <button onClick={() => setShowChat(false)}>✖</button>
          </div>
          <ChatBox polygonContext={polygonContext} />
        </div>
      )}

      {/* Toggle button (when chat is hidden) */}
      {!showChat && (
        <button
          onClick={() => setShowChat(true)}
          style={{
            position: "absolute",
            top: "1rem",
            right: "1rem",
            padding: "0.5rem 1rem",
            background: "#0078d7",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Open Chat
        </button>
      )}
    </div>
  );
}

export default App;
