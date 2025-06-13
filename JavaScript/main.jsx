import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

function ClockWithWindow() {
  const [time, setTime] = useState("--:--");
  const [isDaytime, setIsDaytime] = useState(true);

  useEffect(() => {
    const fetchTime = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/time");
        const data = await response.json();

        // Extract only hours and minutes
        const [hour, minute] = data.time.split(":");
        setTime(`${hour}:${minute}`);
        setIsDaytime(data.is_daytime);
      } catch (error) {
        console.error("Error fetching time:", error);
      }
    };

    fetchTime(); // Initial load
    const interval = setInterval(fetchTime, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "20px",
        backgroundColor: isDaytime ? "#cde4ff" : "#1a1a2e",
        color: isDaytime ? "#000" : "#fff",
        alignItems: "center",
      }}
    >
      <div style={{ fontSize: "2rem", fontWeight: "bold" }}>
        {time}
      </div>

      <div style={{ textAlign: "center" }}>
        <p style={{ margin: 0 }}>{isDaytime ? "☀️ Daytime" : "🌙 Nighttime"}</p>
      </div>

      <div
        style={{
          width: "80px",
          height: "80px",
          borderRadius: "8px",
          backgroundColor: isDaytime ? "#aee1f9" : "#020202",
          border: "3px solid white",
          boxShadow: isDaytime
            ? "0 0 20px #fff5d7 inset"
            : "0 0 30px #0ff inset",
        }}
      ></div>
    </div>
  );
}

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<ClockWithWindow />);