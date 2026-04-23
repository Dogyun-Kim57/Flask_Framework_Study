from flask import Blueprint, request

# 공통 응답 처리 클래스 (render, redirect)
from app.common.response import Response

# 입력값 검증 실패 시 사용하는 예외
from app.common.exceptions import ValidationError

# 회원가입 / 로그인 로직 처리 서비스
from app.services.auth_service import AuthService

# 세션 관리 전담 클래스
from app.common.session_manager import SessionManager


# auth 관련 URL 그룹 생성
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    회원가입 라우트

    GET:
    - 회원가입 페이지 출력

    POST:
    - 입력값 받아서 회원가입 처리
    - 성공 시 로그인 페이지로 이동
    - 실패 시 에러 메시지 출력
    """

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            AuthService.signup(username, email, password)
            return Response.redirect("auth.login")

        except ValidationError as e:
            return Response.render(
                "auth/signup.html",
                error=str(e),
                username=username,
                email=email
            )

    return Response.render("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    로그인 라우트

    GET:
    - 로그인 화면 출력

    POST:
    - 아이디/비밀번호 검증
    - 성공 시 session 저장
    - 홈으로 이동
    """

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = AuthService.login(username, password)
            SessionManager.login(user)
            return Response.redirect("main.index")

        except ValidationError as e:
            return Response.render(
                "auth/login.html",
                error=str(e),
                username=username
            )

    return Response.render("auth/login.html")


@auth_bp.route("/logout")
def logout():
    """
    로그아웃 라우트
    """
    SessionManager.logout()
    return Response.redirect("main.index")