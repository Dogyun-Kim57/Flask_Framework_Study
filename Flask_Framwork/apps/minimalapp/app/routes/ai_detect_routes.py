from flask import Blueprint, current_app

from app.common.response import Response

ai_detect_bp = Blueprint("ai_detect", __name__, url_prefix="/ai-detect")


@ai_detect_bp.route("/aistream")
def ai_stream():
    """
    실시간 탐지 페이지

    역할:
    - 템플릿 렌더링
    - config에 정의된 카메라 목록 전달
    """
    cameras = current_app.config.get("RTSP_CAMERAS", {})

    return Response.render(
        "ai_detect/ai_stream.html",
        cameras=cameras
    )