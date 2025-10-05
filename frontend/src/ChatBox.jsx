import React, { useState } from "react";

function ChatBox({ polygonContext }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          context: polygonContext || {}
        }),
      });
      const data = await resp.json();
      setMessages([...newMessages, { role: "assistant", content: data.reply }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "⚠️ Error contacting server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "1rem", flex: 1 }}>
      <div
        style={{
          height: "300px",
          overflowY: "auto",
          marginBottom: "1rem",
          background: "#fafafa",
          padding: "0.5rem",
        }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              textAlign: m.role === "user" ? "right" : "left",
              margin: "0.5rem 0",
            }}
          >
            <strong>{m.role === "user" ? "You" : "AI"}:</strong> {m.content}
          </div>
        ))}
        {loading && <div><em>AI is typing…</em></div>}
      </div>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type a message..."
        style={{ width: "75%", marginRight: "0.5rem" }}
      />
      <button onClick={sendMessage} disabled={loading}>
        Send
      </button>
    </div>
  );
}

export default ChatBox;
