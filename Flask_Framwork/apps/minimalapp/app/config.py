import os


class Config:
    """
    전체 애플리케이션 환경설정 클래스

    역할:
    - Flask 기본 설정
    - DB 설정
    - 메일 설정
    - 업로드 설정
    - RTSP 카메라 목록 설정
    """

    # Flask 기본 보안 키
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # SQLite DB 연결
    # Flask에서는 sqlite:///minimalapp.db 라고 적어도
    # 실제 instance 폴더 기준으로 잡히는 경우가 많으므로
    # 로그로 실제 경로를 확인하는 습관이 좋다.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///minimalapp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 메일 설정
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

    # 파일 업로드 설정
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png", "jpg", "jpeg", "gif",
        "pdf", "txt", "zip",
        "mp4", "mov",
        "doc", "docx", "xls", "xlsx"
    }

    # =========================
    # 여러 IP 카메라 관리용 설정
    # =========================
    # key:
    #   내부 식별자. 서버/프론트에서 이 값으로 카메라를 구분한다.
    #
    # name:
    #   화면에 표시할 이름
    #
    # url:
    #   실제 RTSP 주소
    #
    # enabled:
    #   초기 사용 가능 여부
    #
    # 주의:
    # 실제 운영에서는 비밀번호를 코드에 직접 넣지 않고
    # 환경변수나 별도 보안 저장소를 쓰는 게 좋다.
    RTSP_CAMERAS = {
        "cam1": {
            "name": "1번 카메라",
            "url": "rtsp://admin:Mbc320!!@192.168.0.38:554/channel=0_stream=0&onvif=0.sdp?real_stream",
            "enabled": True,
        },
        "cam2": {
            "name": "2번 카메라",
            "url": "rtsp://admin:Mbc320!!@192.168.0.43:554/channel=0_stream=1&onvif=0.sdp?real_stream",
            "enabled": True,
        },
    }