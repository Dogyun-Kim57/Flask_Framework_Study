# created_at 기본값 생성을 위해 datetime 사용
from datetime import datetime

# SQLAlchemy 객체 import
from app.extensions import db


class User(db.Model):
    """
    회원 정보를 저장하는 users 테이블 모델

    현재 역할:
    - 회원가입 / 로그인 대상 사용자 정보 저장
    - 세션 저장 시 username, email, role의 기준 데이터가 됨
    - 관리자 / 일반회원 분기에도 사용됨
    """

    # 실제 DB 테이블명 지정
    __tablename__ = "users"

    # 회원 PK
    id = db.Column(db.Integer, primary_key=True)

    # 로그인용 아이디 (중복 불가)
    username = db.Column(db.String(50), nullable=False, unique=True)

    # 이메일 (중복 불가)
    email = db.Column(db.String(100), nullable=False, unique=True)

    # 비밀번호는 평문이 아니라 해시값만 저장
    password_hash = db.Column(db.String(255), nullable=False)

    # 🔥 권한 컬럼 추가
    # - user  : 일반 회원
    # - admin : 관리자
    # 기본값은 일반 회원(user)
    role = db.Column(db.String(20), nullable=False, default="user")

    # 생성일
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # User 1 : N Contact 관계
    # 한 사용자는 여러 개의 문의를 남길 수 있다.
    contacts = db.relationship("Contact", back_populates="user", lazy=True)

    def __repr__(self):
        """
        디버깅 시 객체를 보기 쉽게 표현
        """
        return f"<User {self.id} {self.username} {self.role}>"