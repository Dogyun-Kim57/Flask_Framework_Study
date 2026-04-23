import { socket } from "./socket.js";

export function initRtspStatus() {
  socket.on("rtsp_status", (data) => {
    console.log("[RTSP STATUS]", data);

    if (!data || !data.camera_id || !data.status) {
      return;
    }

    const cameraId = data.camera_id;
    const status = data.status;

    const statusEl = document.getElementById(`rtsp-status-${cameraId}`);
    const streamImage = document.getElementById(`stream-${cameraId}`);
    const placeholder = document.getElementById(`stream-placeholder-${cameraId}`);

    if (!statusEl) {
      return;
    }

    if (status === "running") {
      statusEl.textContent = "실행 중";
      statusEl.classList.remove("stopped");
      statusEl.classList.add("running");
    } else {
      statusEl.textContent = "중지됨";
      statusEl.classList.remove("running");
      statusEl.classList.add("stopped");

      // 스트림 종료 시 UI 초기화
      if (streamImage) {
        streamImage.style.display = "none";
        streamImage.src = "";
      }

      if (placeholder) {
        placeholder.style.display = "flex";
        placeholder.textContent = "IP 카메라가 중지되었습니다.";
      }
    }
  });
}