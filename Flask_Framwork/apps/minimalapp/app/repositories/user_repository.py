# DB 세션 사용을 위해 db import
from app.extensions import db

# User 모델 import
from app.models.user import User


class UserRepository:
    """
    회원 관련 DB 접근 전담 클래스

    역할:
    - 회원 조회
    - 회원 저장
    - 전체 회원 목록 조회
    """

    @staticmethod
    def find_by_id(user_id):
        """
        user_id로 회원 1명 조회
        """
        return User.query.get(user_id)

    @staticmethod
    def find_by_username(username):
        """
        username 기준 회원 1명 조회
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        """
        email 기준 회원 1명 조회
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_all():
        """
        전체 회원 조회
        - 관리자 회원 관리 페이지에서 사용
        - 최신 가입순으로 정렬
        """
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def save(username, email, password_hash, role="user"):
        """
        새로운 회원 저장

        기본 role은 user
        필요 시 관리자 계정을 직접 넣을 수도 있음
        """
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return user