// rtsp_stream.js
// RTSP 영상 처리 전담
import { socket } from "./socket.js";

export function initRtspStream() {
  // 페이지에 있는 모든 카메라 카드 조회
  const cameraCards = document.querySelectorAll(".camera-card");

  cameraCards.forEach((card) => {
    const cameraId = card.dataset.cameraId;

    const streamImage = document.getElementById(`stream-${cameraId}`);
    const streamPlaceholder = document.getElementById(`stream-placeholder-${cameraId}`);

    // 카메라별 이벤트명 구독
    // 예: ai_frame_cam1, ai_frame_cam2
    socket.on(`ai_frame_${cameraId}`, (data) => {
      console.log(`[FRAME RECEIVED][${cameraId}]`, data);

      if (data && data.image) {
        streamPlaceholder.style.display = "none";
        streamImage.style.display = "block";
        streamImage.src = "data:image/jpeg;base64," + data.image;
      }
    });
  });
}