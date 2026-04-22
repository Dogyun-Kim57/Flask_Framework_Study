from flask import Flask

from app.config import Config
from app.extensions import db, migrate, mail, socketio


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="threading")

    # 기존 블루프린트
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.contact_routes import contact_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.member_routes import member_bp
    from app.routes.post_routes import post_bp

    # 실시간 탐지 블루프린트
    from app.routes.ai_detect_routes import ai_detect_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(ai_detect_bp)

    register_socket_events(socketio, app)

    return app


def register_socket_events(socketio, app):
    from app.services.ai_stream_service import AiStreamService

    def run_ai_logic():
        rtsp_url = app.config.get("RTSP_URL")
        print("[SYSTEM] AI Background Task Start")
        print(f"[RTSP] try: {rtsp_url}")
        AiStreamService.run_rtsp_stream(socketio, rtsp_url)

    @socketio.on("connect")
    def handle_connect():
        print("[SOCKET] client connected")

        if not AiStreamService.is_running():
            socketio.start_background_task(run_ai_logic)

    @socketio.on("disconnect")
    def handle_disconnect():
        print("[SOCKET] client disconnected")

    @socketio.on("set_detection_target")
    def handle_target(data):
        target = (data or {}).get("target", "")
        AiStreamService.set_target(target)