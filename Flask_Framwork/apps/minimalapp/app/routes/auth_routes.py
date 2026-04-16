from flask import Blueprint, request

# 공통 응답 처리 클래스 (render, redirect)
from app.common.response import Response

# 입력값 검증 실패 시 사용하는 예외
from app.common.exceptions import ValidationError

# 회원가입 / 로그인 로직 처리 서비스
from app.services.auth_service import AuthService

# 🔥 세션 관리 전담 클래스 (핵심 변경 포인트)
from app.common.session_manager import SessionManager


# auth 관련 URL 그룹 생성
# url_prefix="/auth" → 모든 URL이 /auth로 시작
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
        # HTML form에서 전달된 값 가져오기
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # 회원가입 처리 (검증 + DB 저장)
            AuthService.signup(username, email, password)

            # 성공 시 로그인 페이지로 이동
            return Response.redirect("auth.login")

        except ValidationError as e:
            # 입력값 오류 발생 시 다시 회원가입 페이지 렌더링
            # 기존 입력값 유지
            return Response.render(
                "auth/signup.html",
                error=str(e),
                username=username,
                email=email
            )

    # GET 요청이면 단순 화면 출력
    return Response.render("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    로그인 라우트

    GET:
    - 로그인 화면 출력

    POST:
    - 아이디/비밀번호 검증
    - 성공 시 session 저장 (SessionManager 사용)
    - 홈으로 이동
    """

    if request.method == "POST":
        # 폼 데이터 수집
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            # 로그인 검증 및 사용자 조회
            user = AuthService.login(username, password)

            # 🔥 핵심: 세션 저장을 직접 하지 않고 SessionManager 사용
            SessionManager.login(user)

            # 로그인 성공 후 홈으로 이동
            return Response.redirect("main.index")

        except ValidationError as e:
            # 로그인 실패 시 에러 메시지와 함께 다시 렌더링
            return Response.render(
                "auth/login.html",
                error=str(e),
                username=username
            )

    # GET 요청이면 로그인 화면 출력
    return Response.render("auth/login.html")


@auth_bp.route("/logout")
def logout():
    """
    로그아웃 라우트

    역할:
    - session 제거 (SessionManager 사용)
    - 홈으로 이동
    """

    # 🔥 세션 전체 삭제
    SessionManager.logout()

    # 홈으로 이동
    return Response.redirect("main.index")