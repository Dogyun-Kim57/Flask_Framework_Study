from app.extensions import db
from app.models.detection import Detection


class DetectionRepository:
    """
    Detection 테이블 DB 접근 전용 계층

    역할:
    - 저장
    - 전체 목록 조회
    - 라벨 검색
    - alert만 조회
    - 상세 조회
    """

    @staticmethod
    def save(
        label,
        confidence,
        target_label=None,
        is_target_match=False,
        is_alert=False,
        camera_id=None,
        camera_name=None,
        source_type="rtsp",
        x1=None,
        y1=None,
        x2=None,
        y2=None,
    ):
        """
        탐지 결과 1건 저장
        """
        detection = Detection(
            label=label,
            confidence=confidence,
            target_label=target_label,
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

        db.session.add(detection)
        db.session.commit()
        return detection

    @staticmethod
    def find_all_paginated(page=1, per_page=20):
        """
        전체 탐지 목록 조회
        최신순 정렬
        """
        return (
            Detection.query
            .order_by(Detection.detected_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def find_alerts_paginated(page=1, per_page=20):
        """
        alert 발생 건만 조회
        """
        return (
            Detection.query
            .filter_by(is_alert=True)
            .order_by(Detection.detected_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def find_by_label_paginated(label, page=1, per_page=20):
        """
        라벨 검색
        """
        return (
            Detection.query
            .filter(Detection.label.ilike(f"%{label}%"))
            .order_by(Detection.detected_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def find_by_camera_paginated(camera_id, page=1, per_page=20):
        """
        특정 카메라 기준 탐지 목록 조회
        """
        return (
            Detection.query
            .filter_by(camera_id=camera_id)
            .order_by(Detection.detected_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    @staticmethod
    def find_by_id(detection_id):
        """
        상세 조회
        """
        return Detection.query.get(detection_id)