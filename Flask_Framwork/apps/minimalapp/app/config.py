import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///minimalapp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png", "jpg", "jpeg", "gif",
        "pdf", "txt", "zip",
        "mp4", "mov",
        "doc", "docx", "xls", "xlsx"
    }

    # 여기만 바꿔가면서 테스트
    RTSP_URL = "rtsp://admin:Mbc320!!@192.168.0.43:554/channel=0_stream=1&onvif=0.sdp?real_stream"