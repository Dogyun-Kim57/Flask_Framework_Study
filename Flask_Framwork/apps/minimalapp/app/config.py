# 환경변수를 읽기 위해 os 모듈 사용
import os


class Config:
    """
    Flask 앱 전체 설정 클래스

    - SECRET_KEY : 세션/보안용 키
    - SQLALCHEMY_DATABASE_URI : DB 연결 주소
    - MAIL_* : 메일 발송용 SMTP 설정
    """

    # 세션 서명 등에 사용되는 비밀키
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # DB 연결 주소
    # 환경변수 없으면 sqlite 파일 DB 사용
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///minimalapp.db")

    # SQLAlchemy의 이벤트 추적 기능 비활성화
    # 불필요한 메모리 사용을 줄이기 위해 보통 False로 둔다.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 메일 서버 설정
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # 메일 발신자 주소
    # 따로 지정하지 않으면 MAIL_USERNAME 값을 사용
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    # 문의 메일을 받을 관리자 이메일
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

    # 게시판 업로드 설정
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 전체 요청 최대 50MB

    ALLOWED_EXTENSIONS = {
        "png", "jpg", "jpeg", "gif",
        "pdf", "txt", "zip",
        "mp4", "mov",
        "doc", "docx", "xls", "xlsx"
    }