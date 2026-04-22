from flask import Blueprint
from app.common.response import Response

ai_detect_bp = Blueprint("ai_detect", __name__, url_prefix="/ai-detect")


@ai_detect_bp.route("/aistream")
def ai_stream():
    return Response.render("ai_detect/ai_stream.html")