from sqlalchemy import func

from app.extensions import db
from app.models.detection import Detection


class DetectionDashboardService:
    """
    관리자 전용 탐지 현황 대시보드 서비스

    이 서비스의 목적:
    - DB에 저장된 탐지 데이터를 '화면에 바로 쓰기 좋은 형태'로 가공한다.
    - route에서 직접 집계 쿼리를 길게 작성하지 않도록 분리한다.
    - 나중에 통계 로직이 복잡해져도 이 파일 안에서 관리할 수 있게 한다.

    여기서 다루는 대표 데이터:
    - 전체 탐지 건수
    - 전체 알림 건수
    - 카메라 수
    - 라벨 종류 수
    - 카메라별 탐지 건수
    - 라벨별 탐지 건수
    - 최근 탐지 목록
    """

    @staticmethod
    def get_summary():
        """
        대시보드 상단 요약 카드에 들어갈 데이터를 계산한다.

        반환 예시:
        {
            "total_detections": 262,
            "total_alerts": 41,
            "unique_cameras": 2,
            "unique_labels": 5,
        }

        왜 필요한가?
        - 관리자가 대시보드에 들어오자마자 전체 현황을 한눈에 볼 수 있게 하기 위해
        """
        # 전체 탐지 수
        total_detections = db.session.query(func.count(Detection.id)).scalar() or 0

        # alert=True 인 탐지 건수
        total_alerts = (
            db.session.query(func.count(Detection.id))
            .filter(Detection.is_alert == True)
            .scalar()
            or 0
        )

        # 탐지 기록에 등장한 서로 다른 camera_id 수
        unique_cameras = (
            db.session.query(func.count(func.distinct(Detection.camera_id)))
            .scalar()
            or 0
        )

        # 탐지 기록에 등장한 서로 다른 label 수
        unique_labels = (
            db.session.query(func.count(func.distinct(Detection.label)))
            .scalar()
            or 0
        )

        return {
            "total_detections": total_detections,
            "total_alerts": total_alerts,
            "unique_cameras": unique_cameras,
            "unique_labels": unique_labels,
        }

    @staticmethod
    def get_recent_detections(limit=10):
        """
        최근 탐지 기록 N건 조회

        왜 필요한가?
        - 관리자가 '방금 어떤 탐지가 들어왔는지' 빠르게 확인할 수 있게 하기 위해
        - 상세 페이지로 이동하는 최근 활동 목록 역할도 한다.
        """
        return (
            Detection.query
            .order_by(Detection.detected_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_camera_stats():
        """
        카메라별 탐지 건수 집계

        반환 예시:
        [
            {"camera_id": "cam1", "camera_name": "1번 카메라", "count": 140},
            {"camera_id": "cam2", "camera_name": "2번 카메라", "count": 122},
        ]

        왜 필요한가?
        - 어떤 카메라에서 탐지가 많이 발생하는지 파악하기 위해
        - 카메라별 환경 차이, 노이즈, 설치 위치 문제를 파악하는 데 도움이 된다.
        """
        rows = (
            db.session.query(
                Detection.camera_id,
                Detection.camera_name,
                func.count(Detection.id).label("count")
            )
            .group_by(Detection.camera_id, Detection.camera_name)
            .order_by(func.count(Detection.id).desc())
            .all()
        )

        result = []
        for row in rows:
            result.append({
                "camera_id": row.camera_id,
                "camera_name": row.camera_name or row.camera_id or "-",
                "count": row.count,
            })

        return result

    @staticmethod
    def get_label_stats(limit=10):
        """
        라벨별 탐지 건수 집계

        반환 예시:
        [
            {"label": "person", "count": 180},
            {"label": "laptop", "count": 50},
            {"label": "car", "count": 12},
        ]

        왜 필요한가?
        - 실제로 어떤 객체가 많이 잡히는지 분석하기 위해
        - 타겟 탐지 정확도 및 데이터 특성을 이해하는 데 도움이 된다.
        """
        rows = (
            db.session.query(
                Detection.label,
                func.count(Detection.id).label("count")
            )
            .group_by(Detection.label)
            .order_by(func.count(Detection.id).desc())
            .limit(limit)
            .all()
        )

        result = []
        for row in rows:
            result.append({
                "label": row.label,
                "count": row.count,
            })

        return result

    @staticmethod
    def get_alert_camera_stats():
        """
        alert 발생 건만 카메라별로 집계

        왜 필요한가?
        - 단순 탐지 수가 아니라, 실제로 '중요한 알림'이 어떤 카메라에서 많이 발생하는지 보기 위해
        - 운영 관점에서 더 중요한 지표가 된다.
        """
        rows = (
            db.session.query(
                Detection.camera_id,
                Detection.camera_name,
                func.count(Detection.id).label("count")
            )
            .filter(Detection.is_alert == True)
            .group_by(Detection.camera_id, Detection.camera_name)
            .order_by(func.count(Detection.id).desc())
            .all()
        )

        result = []
        for row in rows:
            result.append({
                "camera_id": row.camera_id,
                "camera_name": row.camera_name or row.camera_id or "-",
                "count": row.count,
            })

        return result