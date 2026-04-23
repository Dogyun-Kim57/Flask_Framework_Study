# Blueprint import
from flask import Blueprint

# 공통 응답 처리 클래스
from app.common.response import Response

# 현재 로그인 사용자명 조회 함수
from app.common.auth import get_current_username

# 메인 블루프린트 생성
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    홈 화면 라우트

    - 로그인 상태면 username 표시
    - 비로그인 상태면 로그인/회원가입 링크 표시
    """

    return Response.render(
        "home/index.html",
        username=get_current_username()
    )