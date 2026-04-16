# Blueprint, request import
from flask import Blueprint, request

# 관리자 권한 체크
from app.common.auth import admin_required

# 공통 응답 클래스
from app.common.response import Response

# DB 세션
from app.extensions import db

# repository import
from app.repositories.contact_repository import ContactRepository
from app.repositories.user_repository import UserRepository

# Contact 모델 import
from app.models.contact import Contact


# 관리자 전용 블루프린트
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/inquiries")
@admin_required
def inquiry_list():
    """
    관리자용 문의 목록 페이지

    역할:
    - 전체 문의 목록 조회
    - 각 문의를 클릭해서 상세 페이지로 이동할 수 있는 기반 화면
    """

    contacts = ContactRepository.find_all()

    return Response.render(
        "admin/inquiry_list.html",
        contacts=contacts
    )


@admin_bp.route("/inquiries/<int:contact_id>", methods=["GET", "POST"])
@admin_required
def inquiry_detail(contact_id):
    """
    관리자용 문의 상세 페이지

    GET:
    - 특정 문의 상세 정보 확인

    POST:
    - 관리자가 답변 내용을 저장
    - 같은 페이지로 다시 리다이렉트하여 최신 답변 내용 반영
    """

    # 문의 1건 조회
    contact = Contact.query.get_or_404(contact_id)

    # 답변 저장 처리
    if request.method == "POST":
        # textarea에서 넘어온 reply 값 수집
        # None 방지를 위해 기본값 "" 사용 후 strip 처리
        reply = request.form.get("reply", "").strip()

        # DB의 reply 컬럼에 답변 저장
        contact.reply = reply

        # 실제 반영
        db.session.commit()

        # 저장 후 다시 상세 페이지로 이동
        return Response.redirect("admin.inquiry_detail", contact_id=contact.id)

    return Response.render(
        "admin/inquiry_detail.html",
        contact=contact
    )


@admin_bp.route("/users")
@admin_required
def user_list():
    """
    관리자용 회원 관리 페이지

    역할:
    - 전체 회원 목록 조회
    - 추후 상세 페이지로 이동 가능
    """

    users = UserRepository.find_all()

    return Response.render(
        "admin/user_list.html",
        users=users
    )

@admin_bp.route("/users/<int:user_id>")
@admin_required
def user_detail(user_id):
    """
    관리자용 회원 상세 페이지

    역할:
    - 특정 회원의 상세 정보 확인
    - 추후 회원 추방 / 관리자 권한 부여 기능 확장 가능
    """

    user = UserRepository.find_by_id(user_id)

    # 사용자가 없으면 메인으로 보내는 대신,
    # 여기서는 간단히 목록으로 돌려보내도 됨
    if not user:
        return Response.redirect("admin.user_list")

    return Response.render(
        "admin/user_detail.html",
        user=user
    )