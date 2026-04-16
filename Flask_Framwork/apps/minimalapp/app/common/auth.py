# 데코레이터 작성 시 원래 함수의 이름/메타정보를 보존하기 위해 wraps 사용
from functools import wraps

# 세션, redirect, url_for 사용
from flask import session, redirect, url_for


def login_required(view_func):
    """
    로그인한 사용자만 접근할 수 있도록 제한하는 데코레이터

    사용 예:
    @login_required
    def contact_history():
        ...
    """

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        # 세션에 user_id가 없으면 로그인 안 된 상태로 판단
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

        # 로그인 상태면 원래 뷰 함수 실행
        return view_func(*args, **kwargs)

    return wrapped_view


def admin_required(view_func):
    """
    관리자만 접근 가능한 데코레이터

    사용 예:
    @admin_required
    def user_list():
        ...

    동작 순서:
    1. 로그인 여부 확인
    2. role == 'admin' 인지 확인
    3. 아니면 메인 페이지로 이동
    """

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        # 로그인 안 되어 있으면 로그인 페이지로
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

        # 로그인은 되어 있지만 관리자가 아니면 메인으로
        if session.get("role") != "admin":
            return redirect(url_for("main.index"))

        return view_func(*args, **kwargs)

    return wrapped_view


def get_current_user_id():
    """
    현재 로그인한 사용자의 id 반환
    로그인하지 않았다면 None 반환
    """
    return session.get("user_id")


def get_current_username():
    """
    현재 로그인한 사용자의 username 반환
    """
    return session.get("username")


def get_current_user_email():
    """
    현재 로그인한 사용자의 이메일 반환
    """
    return session.get("user_email")


def get_current_user_role():
    """
    현재 로그인한 사용자의 권한 반환
    """
    return session.get("role")


def is_admin():
    """
    현재 로그인 사용자가 관리자면 True
    아니면 False
    """
    return session.get("role") == "admin"