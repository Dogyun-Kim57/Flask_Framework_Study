# Blueprint, request, session import
from flask import Blueprint, request, session

# 공통 응답, 예외 import
from app.common.response import Response
from app.common.exceptions import ValidationError

# 인증 관련 공통 함수 import
from app.common.auth import (
    login_required,
    get_current_user_id,
    get_current_username,
    get_current_user_email,
)

# 문의 저장 서비스 / 문의 조회 repository / 메일 서비스 import
from app.services.contact_service import ContactService
from app.services.mail_service import MailService
from app.repositories.contact_repository import ContactRepository

# 문의 관련 블루프린트 생성
contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """
    문의 작성 라우트

    GET:
    - 문의 작성 화면 출력
    - 로그인 사용자 정보 또는 직전 입력값을 기본값으로 보여줌

    POST:
    - 문의 입력값 검증
    - DB 저장
    - 관리자 메일 발송
    - 완료 화면 출력
    """

    if request.method == "POST":
        # 폼 입력값 가져오기
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        description = request.form.get("description", "")

        try:
            # 1) 문의 저장
            saved_contact = ContactService.create_contact(
                user_id=get_current_user_id(),
                name=name,
                email=email,
                description=description
            )

            # 2) 성공적으로 저장된 문의를 세션에 일부 보관
            # 다음 문의 작성 시 이름/이메일 자동 표시용
            session["last_name"] = saved_contact.name
            session["last_email"] = saved_contact.email

            # 3) 관리자 메일 발송
            # 메일 전송 실패까지 사용자 검증 에러로 묶고 싶지 않다면
            # try/except를 따로 분리할 수도 있다.
            MailService.send_contact_email(saved_contact)

            # 4) 완료 화면 출력
            return Response.render(
                "contact/contact_complete.html",
                username=saved_contact.name,
                email=saved_contact.email,
                description=saved_contact.description
            )

        except ValidationError as e:
            # 입력 검증 실패 시 기존 입력값 유지
            return Response.render(
                "contact/contact.html",
                error=str(e),
                username=name,
                email=email,
                description=description
            )

        except Exception:
            # 메일 발송 등 기타 예외 처리
            # 실무에서는 로깅 추가 권장
            return Response.render(
                "contact/contact.html",
                error="문의는 저장되었지만 메일 발송 중 문제가 발생했습니다. 관리자에게 문의해주세요.",
                username=name,
                email=email,
                description=description
            )

    # GET 요청 시 기본값 설정
    # 로그인한 사용자면 회원정보 우선
    # 비로그인 상태면 마지막 문의 입력값 사용
    default_name = get_current_username() or session.get("last_name", "")
    default_email = get_current_user_email() or session.get("last_email", "")

    return Response.render(
        "contact/contact.html",
        username=default_name,
        email=default_email
    )


@contact_bp.route("/contact/history")
@login_required
def contact_history():
    """
    로그인 사용자의 문의 내역 조회 라우트

    - 로그인한 사용자만 접근 가능
    - 해당 사용자의 문의 목록을 최신순으로 조회
    """

    contacts = ContactRepository.find_by_user_id(get_current_user_id())

    return Response.render(
        "contact/contact_history.html",
        contacts=contacts
    )