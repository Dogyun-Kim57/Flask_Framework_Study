# 문의 생성일 기록용
from datetime import datetime

# SQLAlchemy 객체 import
from app.extensions import db


class Contact(db.Model):
    """
    문의 정보를 저장하는 contacts 테이블 모델
    """

    # 실제 DB 테이블명
    __tablename__ = "contacts"

    # 문의 PK
    id = db.Column(db.Integer, primary_key=True)

    # 문의 작성자 회원 id
    # 비회원 문의도 허용하려면 nullable=True 유지
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_contact_user_id"),
        nullable=True
    )

    # 문의자 이름
    name = db.Column(db.String(100), nullable=False)

    # 답변 받을 이메일
    email = db.Column(db.String(255), nullable=False)

    # 문의 본문
    description = db.Column(db.Text, nullable=False)

    # ✅ 추가되는 컬럼 (핵심)
    reply = db.Column(db.Text, nullable=True)

    # 문의 생성 시각
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Contact N : 1 User 관계
    user = db.relationship("User", back_populates="contacts")



    def __repr__(self):
        """
        디버깅 출력용 문자열
        """
        return f"<Contact {self.id} {self.email}>"