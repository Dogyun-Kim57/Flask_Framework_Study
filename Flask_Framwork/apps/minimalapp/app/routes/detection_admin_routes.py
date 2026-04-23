from flask import Blueprint

from app.common.auth import admin_required
from app.common.response import Response
from app.services.detection_dashboard_service import DetectionDashboardService


# 관리자 전용 탐지 현황 블루프린트
# URL 예: /admin/detection/dashboard
detection_admin_bp = Blueprint(
    "detection_admin",
    __name__,
    url_prefix="/admin/detection"
)


@detection_admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """
    관리자 전용 탐지 현황 대시보드 라우트

    동작:
    1. DetectionDashboardService에서 필요한 통계 데이터를 모은다.
    2. 템플릿으로 전달한다.
    3. 관리자는 대시보드 화면에서 요약/통계/최근 탐지를 한 번에 확인할 수 있다.

    왜 admin_required를 쓰는가?
    - 탐지 현황은 일반 사용자보다 관리자가 운영 관점에서 보는 정보이기 때문
    - 카메라별 통계, 알림 현황 등은 관리자 화면에 더 적합하기 때문
    """
    summary = DetectionDashboardService.get_summary()
    recent_detections = DetectionDashboardService.get_recent_detections(limit=10)
    camera_stats = DetectionDashboardService.get_camera_stats()
    label_stats = DetectionDashboardService.get_label_stats(limit=10)
    alert_camera_stats = DetectionDashboardService.get_alert_camera_stats()

    return Response.render(
        "admin/detection/dashboard.html",
        summary=summary,
        recent_detections=recent_detections,
        camera_stats=camera_stats,
        label_stats=label_stats,
        alert_camera_stats=alert_camera_stats,
    )