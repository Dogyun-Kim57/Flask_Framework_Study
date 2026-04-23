import { socket } from "./socket.js";

export function initTarget() {
  const setTargetButtons = document.querySelectorAll(".set-target-btn");

  setTargetButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const cameraId = button.dataset.cameraId;
      const input = document.getElementById(`target-${cameraId}`);

      if (!input) {
        return;
      }

      const target = input.value.trim();

      socket.emit("set_detection_target", {
        camera_id: cameraId,
        target: target
      });

      console.log(`[TARGET SET][${cameraId}]`, target);
    });
  });
}