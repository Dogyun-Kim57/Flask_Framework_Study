# Flask 앱 객체를 만들기 위한 Flask 클래스 import
from flask import Flask

# 프로젝트 설정 클래스 import
from app.config import Config

# DB, 마이그레이션, 메일 확장 객체 import
from app.extensions import db, migrate, mail


def create_app():
    """
    애플리케이션 팩토리 함수

    - Flask 앱 객체 생성
    - 설정 적용
    - 확장 기능 초기화
    - 라우트(블루프린트) 등록
    - 완성된 app 반환
    """

    # Flask 앱 생성
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Config 클래스의 설정값을 Flask 앱에 적용
    app.config.from_object(Config)

    # SQLAlchemy 연결
    db.init_app(app)

    # Flask-Migrate 연결
    migrate.init_app(app, db)

    # Flask-Mail 연결
    mail.init_app(app)

    # 블루프린트 import

    # 순환참조 방지를 위해 함수 내부 import 유지
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.contact_routes import contact_bp

    # 관리자 / 회원 블루프린트
    from app.routes.admin_routes import admin_bp
    from app.routes.member_routes import member_bp

    # 게시판 관련
    from app.routes.post_routes import post_bp


    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)

    # 관리자 / 회원 기능 등록
    app.register_blueprint(admin_bp)
    app.register_blueprint(member_bp)

    # 게시판
    app.register_blueprint(post_bp)

    return app