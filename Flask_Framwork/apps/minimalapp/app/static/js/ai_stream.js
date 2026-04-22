const socket = io();

const streamImage = document.getElementById("stream");
const streamPlaceholder = document.getElementById("stream-placeholder");
const alertBox = document.getElementById("alert");
const targetInput = document.getElementById("target");
const setTargetBtn = document.getElementById("set-target-btn");

socket.on("connect", () => {
  console.log("[SOCKET] connected");
});

socket.on("ai_frame", (data) => {
  console.log("[FRAME RECEIVED]", data);

  if (data && data.image) {
    streamPlaceholder.style.display = "none";
    streamImage.style.display = "block";
    streamImage.src = "data:image/jpeg;base64," + data.image;
  }
});

socket.on("detection_alert", (data) => {
  console.log("[ALERT RECEIVED]", data);

  if (data && data.label && data.time) {
    alertBox.textContent = `[${data.time}] ${data.label} 탐지됨`;
  }
});

setTargetBtn.addEventListener("click", () => {
  const target = targetInput.value.trim();

  socket.emit("set_detection_target", {
    target: target
  });
});