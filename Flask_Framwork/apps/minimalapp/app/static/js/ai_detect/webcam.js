export function initWebcam() {
  const webcamVideo = document.getElementById("webcam");
  const webcamPlaceholder = document.getElementById("webcam-placeholder");

  const startBtn = document.getElementById("start-webcam-btn");
  const stopBtn = document.getElementById("stop-webcam-btn");

  let webcamStream = null;

  async function startWebcam() {
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
      });

      webcamVideo.srcObject = webcamStream;
      webcamPlaceholder.style.display = "none";
      webcamVideo.style.display = "block";

      console.log("[WEBCAM] started");
    } catch (error) {
      console.error("[WEBCAM ERROR]", error);
      webcamPlaceholder.style.display = "flex";
      webcamPlaceholder.textContent = "웹캠에 접근할 수 없습니다. 브라우저 권한을 확인해주세요.";
      webcamVideo.style.display = "none";
    }
  }

  function stopWebcam() {
    if (webcamStream) {
      webcamStream.getTracks().forEach(track => track.stop());
      webcamStream = null;
    }

    webcamVideo.srcObject = null;
    webcamVideo.style.display = "none";
    webcamPlaceholder.style.display = "flex";
    webcamPlaceholder.textContent = "웹캠이 종료되었습니다.";

    console.log("[WEBCAM] stopped");
  }

  if (startBtn) {
    startBtn.addEventListener("click", startWebcam);
  }

  if (stopBtn) {
    stopBtn.addEventListener("click", stopWebcam);
  }

  window.addEventListener("beforeunload", stopWebcam);
}