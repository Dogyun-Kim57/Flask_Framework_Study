from flask import Blueprint, request

from app.common.response import Response
from app.services.traffic_cctv_service import TrafficCctvService


traffic_bp = Blueprint("traffic", __name__, url_prefix="/traffic")


@traffic_bp.route("/cctv")
def traffic_cctv_page():
    """
    실시간 교통 탐지 페이지
    """
    return Response.render("traffic/traffic_cctv.html")


@traffic_bp.route("/api/cctv")
def traffic_cctv_api():
    """
    CCTV 목록 JSON API

    프론트 JS에서 호출한다.
    API 키는 프론트로 노출하지 않는다.
    """

    min_x = request.args.get("minX", "126.70")
    max_x = request.args.get("maxX", "127.20")
    min_y = request.args.get("minY", "37.30")
    max_y = request.args.get("maxY", "37.70")
    road_type = request.args.get("roadType", "all")
    cctv_type = request.args.get("cctvType", "4")

    try:
        cctv_list = TrafficCctvService.get_cctv_list(
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            road_type=road_type,
            cctv_type=cctv_type
        )

        return Response.json_success(
            message="CCTV 목록 조회 성공",
            data=cctv_list
        )

    except Exception as e:
        return Response.json_error(
            message=f"CCTV 목록 조회 실패: {str(e)}",
            status=500
        )