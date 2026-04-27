# Blueprint, request import
from flask import Blueprint, request

# 관리자 권한 체크
from app.common.auth import admin_required, get_current_user_id

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
    """

    contacts = ContactRepository.find_all()

    return Response.render(
        "admin/inquiry/list.html",
        contacts=contacts
    )


@admin_bp.route("/inquiries/<int:contact_id>", methods=["GET", "POST"])
@admin_required
def inquiry_detail(contact_id):
    """
    관리자용 문의 상세 페이지
    """

    contact = Contact.query.get_or_404(contact_id)

    if request.method == "POST":
        reply = request.form.get("reply", "").strip()
        contact.reply = reply
        db.session.commit()

        return Response.redirect("admin.inquiry_detail", contact_id=contact.id)

    return Response.render(
        "admin/inquiry/detail.html",
        contact=contact
    )


@admin_bp.route("/users")
@admin_required
def user_list():
    """
    관리자용 회원 관리 페이지
    """

    users = UserRepository.find_all()

    return Response.render(
        "admin/user/list.html",
        users=users
    )


@admin_bp.route("/users/<int:user_id>")
@admin_required
def user_detail(user_id):
    """
    관리자용 회원 상세 페이지
    """

    user = UserRepository.find_by_id(user_id)

    if not user:
        return Response.redirect("admin.user_list")

    return Response.render(
        "admin/user/detail.html",
        user=user
    )

@admin_bp.route("/users/<int:user_id>/promote", methods=["POST"])
@admin_required
def promote_user(user_id):
    user = UserRepository.find_by_id(user_id)

    if not user:
        return Response.redirect("admin.user_list")

    # 이미 관리자면 다시 올릴 필요 없음
    if user.role == "admin":
        return Response.redirect("admin.user_detail", user_id=user.id)

    # 자기 자신에게 승격 버튼을 누르는 경우도 그냥 막아도 되고,
    # 허용해도 되지만 여기서는 불필요하므로 막음
    if user.id == get_current_user_id():
        return Response.redirect("admin.user_detail", user_id=user.id)

    UserRepository.promote_to_admin(user)

    return Response.redirect("admin.user_detail", user_id=user.id)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = UserRepository.find_by_id(user_id)

    if not user:
        return Response.redirect("admin.user_list")

    # 자기 자신 추방 방지
    if user.id == get_current_user_id():
        return Response.redirect("admin.user_detail", user_id=user.id)

    UserRepository.delete(user)

    return Response.redirect("admin.user_list")