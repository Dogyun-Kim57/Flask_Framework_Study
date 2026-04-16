# DB 세션 import
from app.extensions import db

# Contact 모델 import
from app.models.contact import Contact


class ContactRepository:
    """
    문의 관련 DB 접근 전담 클래스

    역할:
    - 문의 저장
    - 이메일 기준 조회
    - 사용자 기준 문의 내역 조회
    - 전체 문의 조회
    """

    @staticmethod
    def save(user_id, name, email, description):
        """
        문의 저장
        """
        contact = Contact(
            user_id=user_id,
            name=name,
            email=email,
            description=description
        )

        db.session.add(contact)
        db.session.commit()

        return contact

    @staticmethod
    def find_by_email(email):
        """
        특정 이메일로 작성된 문의 목록 조회
        최신순으로 정렬
        """
        return Contact.query.filter_by(email=email).order_by(Contact.created_at.desc()).all()

    @staticmethod
    def find_by_user_id(user_id):
        """
        특정 사용자(user_id)의 문의 목록 조회
        최신순으로 정렬
        """
        return Contact.query.filter_by(user_id=user_id).order_by(Contact.created_at.desc()).all()

    @staticmethod
    def find_all():
        """
        전체 문의 목록 조회
        - 관리자 문의 관리 페이지에서 사용
        - 최신순 정렬
        """
        return Contact.query.order_by(Contact.created_at.desc()).all()