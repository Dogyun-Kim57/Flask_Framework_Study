import base64
import os
import time

import cv2
import torch
from ultralytics import YOLO

from app.services.detection_service import DetectionService


class AiStreamService:
    """
    여러 RTSP 카메라를 동시에 관리하는 실시간 탐지 서비스

    기존 단일 카메라 구조와 달라진 점:
    - _is_running 같은 단일 상태가 아니라
      카메라별 상태를 dict로 관리한다.
    - camera_id를 기준으로 시작/종료/상태/target을 분리 관리한다.

    관리 대상:
    - 실행 여부
    - 종료 요청 여부
    - 상태 문자열
    - 카메라별 target 라벨
    """

    _model = None
    _device = "cuda" if torch.cuda.is_available() else "cpu"

    # 카메라별 실행 상태
    # 예: {"cam1": True, "cam2": False}
    _running_map = {}

    # 카메라별 종료 요청 상태
    # 예: {"cam1": False, "cam2": True}
    _stop_requested_map = {}

    # 카메라별 상태 문자열
    # running / stopped
    _status_map = {}

    # 카메라별 target 라벨
    # 예: {"cam1": "person", "cam2": "car"}
    _target_map = {}

    @classmethod
    def load_model(cls):
        """
        YOLO 모델 1회 로딩 후 재사용
        """
        if cls._model is None:
            cls._model = YOLO("yolov8n.pt")
            cls._model.to(cls._device)
            print(f"[AI] Model Loaded on: {cls._device}")
        return cls._model

    @classmethod
    def is_running(cls, camera_id):
        """
        특정 카메라가 현재 실행 중인지 반환
        """
        return cls._running_map.get(camera_id, False)

    @classmethod
    def get_status(cls, camera_id):
        """
        특정 카메라 현재 상태 반환
        기본값은 stopped
        """
        return cls._status_map.get(camera_id, "stopped")

    @classmethod
    def set_target(cls, camera_id, label):
        """
        특정 카메라 감시 대상(target) 설정
        """
        cls._target_map[camera_id] = (label or "").strip().lower()
        print(f"[AI] Target set for {camera_id}: {cls._target_map[camera_id]}")

    @classmethod
    def get_target(cls, camera_id):
        """
        특정 카메라 target 반환
        """
        return cls._target_map.get(camera_id, "")

    @classmethod
    def request_stop(cls, camera_id):
        """
        특정 카메라 종료 요청
        """
        cls._stop_requested_map[camera_id] = True
        print(f"[AI] Stop requested for {camera_id}")

    @classmethod
    def run_rtsp_stream(cls, socketio, camera_id, camera_name, rtsp_url):
        """
        특정 카메라 RTSP 스트림 실행

        흐름:
        1. 카메라 연결
        2. 프레임 읽기
        3. 주기적으로 YOLO 추론
        4. 카메라별 Socket 이벤트 전송
        5. DB 저장
        6. target 일치 시 알림 전송
        7. 종료 요청 시 안전 종료
        """
        if cls.is_running(camera_id):
            print(f"[AI] Stream already running for {camera_id}")
            return

        cls._running_map[camera_id] = True
        cls._stop_requested_map[camera_id] = False
        cls._status_map[camera_id] = "running"

        # 모든 클라이언트에게 해당 카메라 상태 브로드캐스트
        socketio.emit("rtsp_status", {
            "camera_id": camera_id,
            "status": "running"
        })

        cap = None

        try:
            if not rtsp_url:
                print(f"[ERROR] RTSP_URL is empty for {camera_id}")
                return

            # RTSP를 TCP로 받도록 설정
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            print(f"[RTSP] {camera_id} opened: {cap.isOpened()}")

            if not cap.isOpened():
                print(f"[ERROR] RTSP 연결 실패: {camera_id} / {rtsp_url}")
                return

            model = cls.load_model()
            frame_count = 0
            last_alert_time = 0

            print(f"[START] {camera_id} AI 모니터링 시작 (Device: {cls._device})")

            while cap.isOpened():
                # 관리자 종료 요청이 들어오면 루프 중단
                if cls._stop_requested_map.get(camera_id, False):
                    print(f"[AI] Stop signal received for {camera_id}")
                    break

                ret, frame = cap.read()

                if not ret:
                    socketio.sleep(0.1)
                    continue

                frame = cv2.resize(frame, (640, 480))
                frame_count += 1

                annotated_frame = frame
                boxes = None

                # 3프레임당 1번만 추론
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

                    # 현재 카메라 target 가져오기
                    target_label = cls.get_target(camera_id)

                    # DB 저장
                    DetectionService.save_detection_results(
                        model=model,
                        boxes=boxes,
                        target_label=target_label,
                        camera_id=camera_id,
                        camera_name=camera_name,
                        source_type="rtsp",
                    )

                # 프레임 인코딩
                success, buffer = cv2.imencode(
                    ".jpg",
                    annotated_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 80]
                )

                if not success:
                    socketio.sleep(0.01)
                    continue

                encoded_image = base64.b64encode(buffer).decode("utf-8")

                # 카메라별 프레임 이벤트명으로 전송
                # 예: ai_frame_cam1, ai_frame_cam2
                socketio.emit(f"ai_frame_{camera_id}", {
                    "camera_id": camera_id,
                    "image": encoded_image,
                    "count": frame_count
                })

                # 카메라별 target 일치 시 알림
                current_target = cls.get_target(camera_id)

                if current_target and boxes is not None:
                    detected_names = [
                        model.names[int(cls_idx)].lower()
                        for cls_idx in boxes.cls.tolist()
                    ]

                    current_time = time.time()

                    if (
                        current_target in detected_names
                        and current_time - last_alert_time > 3
                    ):
                        last_alert_time = current_time

                        socketio.emit("detection_alert", {
                            "camera_id": camera_id,
                            "camera_name": camera_name,
                            "label": current_target,
                            "time": time.strftime("%H:%M:%S")
                        })

                socketio.sleep(0.03)

        except Exception as e:
            print(f"[AI ERROR] {camera_id}: {e}")

        finally:
            if cap is not None:
                cap.release()

            cls._running_map[camera_id] = False
            cls._stop_requested_map[camera_id] = False
            cls._status_map[camera_id] = "stopped"

            socketio.emit("rtsp_status", {
                "camera_id": camera_id,
                "status": "stopped"
            })

            print(f"[AI] Stream stopped for {camera_id}")