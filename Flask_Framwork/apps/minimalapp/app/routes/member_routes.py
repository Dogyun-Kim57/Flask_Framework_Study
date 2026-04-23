# Blueprint, request import
from flask import Blueprint, request

# 로그인 체크, 현재 사용자 id 조회
from app.common.auth import login_required, get_current_user_id

# 공통 응답 클래스
from app.common.response import Response

# DB 세션
from app.extensions import db

# repository import
from app.repositories.user_repository import UserRepository
from app.repositories.contact_repository import ContactRepository

# 모델 import
from app.models.contact import Contact


# 회원 전용 블루프린트
member_bp = Blueprint("member", __name__, url_prefix="/member")


@member_bp.route("/profile")
@login_required
def profile():
    """
    내 계정 정보 확인 페이지
    """

    user = UserRepository.find_by_id(get_current_user_id())

    return Response.render(
        "common/profile/detail.html",
        user=user
    )


@member_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def profile_edit():
    """
    내 계정 정보 수정 페이지
    """

    user = UserRepository.find_by_id(get_current_user_id())

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not username or not email:
            return Response.render(
                "common/profile/edit.html",
                user=user,
                error="아이디와 이메일을 모두 입력해주세요."
            )

        existing_username_user = UserRepository.find_by_username(username)
        if existing_username_user and existing_username_user.id != user.id:
            return Response.render(
                "common/profile/edit.html",
                user=user,
                error="이미 사용 중인 아이디입니다."
            )

        existing_email_user = UserRepository.find_by_email(email)
        if existing_email_user and existing_email_user.id != user.id:
            return Response.render(
                "common/profile/edit.html",
                user=user,
                error="이미 사용 중인 이메일입니다."
            )

        user.username = username
        user.email = email
        db.session.commit()

        return Response.redirect("member.profile")

    return Response.render(
        "common/profile/edit.html",
        user=user
    )


@member_bp.route("/inquiries")
@login_required
def inquiry_list():
    """
    회원 본인의 문의 내역 목록 페이지
    """

    contacts = ContactRepository.find_by_user_id(get_current_user_id())

    return Response.render(
        "member/inquiry/list.html",
        contacts=contacts
    )


@member_bp.route("/inquiries/<int:contact_id>")
@login_required
def inquiry_detail(contact_id):
    """
    회원 본인의 문의 상세 페이지
    """

    contact = Contact.query.get_or_404(contact_id)

    if contact.user_id != get_current_user_id():
        return Response.redirect("main.index")

    return Response.render(
        "member/inquiry/detail.html",
        contact=contact
    )