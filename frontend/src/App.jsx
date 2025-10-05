import React from "react";
import MapView from "./MapView";   
import ChatBox from "./ChatBox"; 

function App() {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left side: Map */}
      <div style={{ flex: 2, borderRight: "1px solid #ccc" }}>
        <MapView />
      </div>

      {/* Right side: Chat */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <h2 style={{ margin: "0.5rem" }}>Assistant Chat</h2>
        <ChatBox />
      </div>
    </div>
  );
}

export default App;
