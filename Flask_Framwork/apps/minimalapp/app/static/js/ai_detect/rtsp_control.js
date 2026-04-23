import { socket } from "./socket.js";

export function initRtspControl() {
  const startButtons = document.querySelectorAll(".start-rtsp-btn");
  const stopButtons = document.querySelectorAll(".stop-rtsp-btn");

  startButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const cameraId = button.dataset.cameraId;

      socket.emit("start_rtsp_stream", {
        camera_id: cameraId
      });

      console.log(`[RTSP START REQUEST][${cameraId}]`);
    });
  });

  stopButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const cameraId = button.dataset.cameraId;

      socket.emit("stop_rtsp_stream", {
        camera_id: cameraId
      });

      console.log(`[RTSP STOP REQUEST][${cameraId}]`);
    });
  });
}