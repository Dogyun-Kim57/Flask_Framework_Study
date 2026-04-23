from datetime import datetime

from app.extensions import db


class Detection(db.Model):
    """
    탐지 결과 저장 테이블

    역할:
    - 어떤 카메라에서 어떤 객체가 탐지됐는지 저장
    - confidence, bbox, target 일치 여부, alert 여부 저장
    - 나중에 탐지 기록 조회 / 통계 / 관리자 화면에 활용
    """

    __tablename__ = "detections"

    # PK
    id = db.Column(db.Integer, primary_key=True)

    # 탐지된 객체 라벨
    # 예: person, car, laptop
    label = db.Column(db.String(100), nullable=False)

    # 모델 confidence
    confidence = db.Column(db.Float, nullable=False, default=0.0)

    # 사용자가 현재 설정한 감시 대상
    # 예: person
    target_label = db.Column(db.String(100), nullable=True)

    # target과 실제 탐지 라벨이 일치했는지
    is_target_match = db.Column(db.Boolean, nullable=False, default=False)

    # 현재 구조에서는 target 일치 시 alert로 간주
    is_alert = db.Column(db.Boolean, nullable=False, default=False)

    # 어떤 카메라에서 나온 탐지인지
    # 예: cam1, cam2
    camera_id = db.Column(db.String(50), nullable=True)

    # 화면 표시용 카메라 이름
    # 예: 정문 카메라
    camera_name = db.Column(db.String(100), nullable=True)

    # 소스 타입
    # 예: rtsp, webcam
    source_type = db.Column(db.String(50), nullable=False, default="rtsp")

    # bbox 좌표
    x1 = db.Column(db.Float, nullable=True)
    y1 = db.Column(db.Float, nullable=True)
    x2 = db.Column(db.Float, nullable=True)
    y2 = db.Column(db.Float, nullable=True)

    # 실제 탐지 시각
    detected_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 생성 시각
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Detection {self.id} {self.camera_id} {self.label} {self.confidence}>"