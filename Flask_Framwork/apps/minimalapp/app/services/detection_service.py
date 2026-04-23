import time

from app.repositories.detection_repository import DetectionRepository

class DetectionService:
    """
    탐지 결과 비즈니스 로직 처리 계층

    역할:
    - YOLO boxes 결과 해석
    - 저장 조건 판단
    - target 일치 여부 판단
    - alert 여부 판단
    - DB 저장 위임
    """

    # 동일 카메라 + 동일 라벨이 너무 자주 쌓이지 않게 하기 위한 캐시
    _last_saved_times = {}

    # 같은 라벨 저장 쿨타임
    _save_cooldown_seconds = 3

    # 너무 낮은 confidence는 저장하지 않음
    _min_confidence = 0.70

    @classmethod
    def save_detection_results(
        cls,
        model,
        boxes,
        target_label="",
        camera_id=None,
        camera_name=None,
        source_type="rtsp",
    ):
        """
        YOLO boxes 결과를 DB에 저장

        매개변수:
        - model:
            YOLO 모델 객체. model.names 로 라벨명을 꺼낸다.
        - boxes:
            results[0].boxes 형태
        - target_label:
            사용자가 현재 감시 대상으로 지정한 라벨
        - camera_id:
            내부 카메라 식별자
        - camera_name:
            화면 표시용 카메라 이름
        - source_type:
            rtsp / webcam 등
        """
        if boxes is None or len(boxes) == 0:
            return []

        saved_items = []
        target_label = (target_label or "").strip().lower()

        for box in boxes:
            # 클래스 index 추출
            cls_idx = int(box.cls.item())

            # confidence 추출
            confidence = float(box.conf.item())

            # 라벨명 추출
            label = str(model.names[cls_idx]).lower()

            # bbox 추출
            xyxy = box.xyxy[0].tolist() if box.xyxy is not None else [None, None, None, None]
            x1, y1, x2, y2 = xyxy

            # target과 일치하는지 판단
            is_target_match = bool(target_label) and label == target_label

            # 현재 구조에서는 target 일치 시 alert로 간주
            is_alert = is_target_match

            # -------------------------
            # 저장 정책 1
            # confidence가 너무 낮으면 저장하지 않음
            # -------------------------
            if confidence < cls._min_confidence:
                continue

            # -------------------------
            # 저장 정책 2
            # 같은 카메라 + 같은 라벨 중복 저장 방지
            # -------------------------
            save_key = f"{camera_id}:{label}"
            now = time.time()
            last_saved_time = cls._last_saved_times.get(save_key, 0)

            if now - last_saved_time < cls._save_cooldown_seconds:
                continue

            saved = DetectionRepository.save(
                label=label,
                confidence=confidence,
                target_label=target_label or None,
                is_target_match=is_target_match,
                is_alert=is_alert,
                camera_id=camera_id,
                camera_name=camera_name,
                source_type=source_type,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
            )

            cls._last_saved_times[save_key] = now
            saved_items.append(saved)

        return saved_items

    @staticmethod
    def get_detection_list(page=1, per_page=20, label="", camera_id=""):
        """
        탐지 목록 조회

        우선순위:
        1. camera_id가 있으면 카메라별 조회
        2. label이 있으면 라벨 검색
        3. 없으면 전체 조회
        """
        camera_id = (camera_id or "").strip()
        label = (label or "").strip()

        if camera_id:
            return DetectionRepository.find_by_camera_paginated(
                camera_id=camera_id,
                page=page,
                per_page=per_page
            )

        if label:
            return DetectionRepository.find_by_label_paginated(
                label=label,
                page=page,
                per_page=per_page
            )

        return DetectionRepository.find_all_paginated(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_alert_list(page=1, per_page=20):
        """
        alert 발생 건 조회
        """
        return DetectionRepository.find_alerts_paginated(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_detection_detail(detection_id):
        """
        탐지 상세 조회
        """
        return DetectionRepository.find_by_id(detection_id)