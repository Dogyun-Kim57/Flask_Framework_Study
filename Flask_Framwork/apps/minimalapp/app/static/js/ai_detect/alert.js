import { socket } from "./socket.js";

export function initAlert() {
  const alertBox = document.getElementById("alert");

  socket.on("detection_alert", (data) => {
    console.log("[ALERT RECEIVED]", data);

    if (!data || !data.label || !data.time) {
      return;
    }

    const cameraName = data.camera_name || data.camera_id || "unknown-camera";

    alertBox.textContent = `[${data.time}] [${cameraName}] ${data.label} 탐지됨`;
  });
}