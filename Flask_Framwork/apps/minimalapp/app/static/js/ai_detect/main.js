// 전체 초기화 파일

import { socket } from "./socket.js";
import { initRtspStream } from "./rtsp_stream.js";
import { initRtspStatus } from "./rtsp_status.js";
import { initTarget } from "./target.js";
import { initRtspControl } from "./rtsp_control.js";
import { initAlert } from "./alert.js";
import { initWebcam } from "./webcam.js";

socket.on("connect", () => {
  console.log("[SOCKET] connected");
});

initRtspStream();
initRtspStatus();
initTarget();
initRtspControl();
initAlert();
initWebcam();