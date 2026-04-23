from flask import Blueprint, request

from app.common.auth import login_required, admin_required
from app.common.response import Response
from app.services.detection_service import DetectionService

detection_bp = Blueprint("detection", __name__, url_prefix="/detections")


@detection_bp.route("")
@login_required
def detection_list():
    """
    탐지 기록 목록 페이지

    지원 기능:
    - 전체 목록
    - 카메라별 조회
    - 라벨 검색
    - 페이징
    """
    page = request.args.get("page", 1, type=int)
    label = request.args.get("label", "", type=str).strip()
    camera_id = request.args.get("camera_id", "", type=str).strip()

    pagination = DetectionService.get_detection_list(
        page=page,
        per_page=20,
        label=label,
        camera_id=camera_id
    )

    return Response.render(
        "detection/list.html",
        detections=pagination.items,
        pagination=pagination,
        keyword=label,
        selected_camera_id=camera_id
    )


@detection_bp.route("/alerts")
@admin_required
def detection_alert_list():
    """
    관리자용 alert 기록 페이지
    """
    page = request.args.get("page", 1, type=int)

    pagination = DetectionService.get_alert_list(
        page=page,
        per_page=20
    )

    return Response.render(
        "detection/list.html",
        detections=pagination.items,
        pagination=pagination,
        keyword="",
        selected_camera_id="",
        alert_mode=True
    )


@detection_bp.route("/<int:detection_id>")
@login_required
def detection_detail(detection_id):
    """
    탐지 상세 페이지
    """
    detection = DetectionService.get_detection_detail(detection_id)

    if not detection:
        return Response.redirect("detection.detection_list")

    return Response.render(
        "detection/detail.html",
        detection=detection
    )