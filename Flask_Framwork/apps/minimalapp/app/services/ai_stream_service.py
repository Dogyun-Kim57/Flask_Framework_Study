import base64
import os
import time

import cv2
import torch
from ultralytics import YOLO


class AiStreamService:
    _model = None
    _target_label = ""
    _device = "cuda" if torch.cuda.is_available() else "cpu"
    _is_running = False

    @classmethod
    def is_running(cls):
        return cls._is_running

    @classmethod
    def load_model(cls):
        if cls._model is None:
            cls._model = YOLO("yolov8n.pt")
            cls._model.to(cls._device)
            print(f"[AI] Model Loaded on: {cls._device}")
        return cls._model

    @classmethod
    def set_target(cls, label):
        cls._target_label = (label or "").strip().lower()
        print(f"[AI] Target set: {cls._target_label}")

    @classmethod
    def run_rtsp_stream(cls, socketio, rtsp_url):
        if cls._is_running:
            print("[AI] Stream already running")
            return

        cls._is_running = True
        cap = None

        try:
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            print(f"[RTSP] opened: {cap.isOpened()}")

            if not cap.isOpened():
                print(f"[ERROR] RTSP 연결 실패: {rtsp_url}")
                return

            model = cls.load_model()
            frame_count = 0
            last_alert_time = 0

            print(f"[START] AI 모니터링 시작 (Device: {cls._device})")

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    socketio.sleep(0.1)
                    continue

                frame = cv2.resize(frame, (640, 480))
                frame_count += 1

                annotated_frame = frame
                boxes = None

                # 3프레임당 1번만 탐지
                if frame_count % 3 == 0:
                    device = 0 if cls._device == "cuda" else "cpu"

                    results = model.predict(
                        frame,
                        device=device,
                        conf=0.7,
                        verbose=False,
                        imgsz=640
                    )

                    boxes = results[0].boxes
                    annotated_frame = results[0].plot()

                success, buffer = cv2.imencode(
                    ".jpg",
                    annotated_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 80]
                )

                if not success:
                    socketio.sleep(0.01)
                    continue

                encoded_image = base64.b64encode(buffer).decode("utf-8")

                socketio.emit("ai_frame", {
                    "image": encoded_image,
                    "count": frame_count
                })

                if cls._target_label and boxes is not None:
                    detected_names = [
                        model.names[int(cls_idx)].lower()
                        for cls_idx in boxes.cls.tolist()
                    ]

                    current_time = time.time()

                    if (
                        cls._target_label in detected_names
                        and current_time - last_alert_time > 3
                    ):
                        last_alert_time = current_time
                        socketio.emit("detection_alert", {
                            "label": cls._target_label,
                            "time": time.strftime("%H:%M:%S")
                        })

                socketio.sleep(0.03)

        except Exception as e:
            print(f"[AI ERROR] {e}")

        finally:
            if cap is not None:
                cap.release()

            cls._is_running = False
            print("[AI] Stream stopped")