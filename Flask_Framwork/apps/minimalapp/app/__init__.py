from flask import Flask

from app.config import Config
from app.extensions import db, migrate, mail, socketio


def create_app():
    """
    Flask 애플리케이션 팩토리 함수

    역할:
    1. Flask 앱 생성
    2. Config 적용
    3. 확장 기능 초기화
    4. 블루프린트 등록
    5. Socket 이벤트 등록
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # 환경설정 적용
    app.config.from_object(Config)

    # 현재 어떤 DB를 쓰는지 디버깅할 때 도움이 되도록 로그 출력
    print("[DB URI]", app.config["SQLALCHEMY_DATABASE_URI"])
    print("[INSTANCE PATH]", app.instance_path)

    # Flask 확장 기능 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="threading")

    # =========================
    # 블루프린트 import
    # =========================
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.contact_routes import contact_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.member_routes import member_bp
    from app.routes.post_routes import post_bp
    from app.routes.ai_detect_routes import ai_detect_bp
    from app.routes.detection_routes import detection_bp

    #  새로 추가된 관리자 전용 탐지 대시보드 블루프린트
    from app.routes.detection_admin_routes import detection_admin_bp

    # ITS 국가교통정보
    from app.routes.traffic_routes import traffic_bp


    # =========================
    # 블루프린트 등록
    # =========================
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(ai_detect_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(detection_admin_bp)
    app.register_blueprint(traffic_bp)


    # Socket 이벤트 등록
    register_socket_events(socketio, app)

    return app


def register_socket_events(socketio, app):
    """
    SocketIO 이벤트 등록 함수

    현재 구조의 핵심:
    - 여러 카메라를 camera_id 기준으로 제어한다.
    - connect 시 현재 카메라 상태를 클라이언트에 전달한다.
    - start_rtsp_stream / stop_rtsp_stream 이벤트로 카메라를 시작/종료한다.
    - set_detection_target 이벤트로 카메라별 target을 설정한다.
    """
    from app.services.ai_stream_service import AiStreamService

    def build_run_ai_logic(camera_id, camera_name, rtsp_url):
        """
        카메라별 백그라운드 실행 함수를 만들어 반환한다.

        왜 필요한가?
        - SocketIO의 start_background_task는 실행할 함수를 넘겨받는다.
        - 카메라별로 다른 id/name/url을 가진 실행 함수를 만들어야 하므로
          내부 함수 형태로 감싸서 반환한다.
        """
        def run_ai_logic():
            # DetectionService -> Repository -> DB 접근까지 들어가기 때문에
            # 앱 컨텍스트 안에서 실행해야 한다.
            with app.app_context():
                print(f"[SYSTEM] AI Background Task Start: {camera_id}")
                print(f"[RTSP] try: {rtsp_url}")

                AiStreamService.run_rtsp_stream(
                    socketio=socketio,
                    camera_id=camera_id,
                    camera_name=camera_name,
                    rtsp_url=rtsp_url
                )

        return run_ai_logic

    @socketio.on("connect")
    def handle_connect():
        """
        소켓 연결 시 실행

        역할:
        - 연결 로그 출력
        - 현재 각 카메라의 running/stopped 상태를 클라이언트에 전달

        왜 필요한가?
        - 페이지 새로고침 후에도 현재 카메라 상태를 UI에 반영하기 위해
        """
        print("[SOCKET] client connected")

        cameras = app.config.get("RTSP_CAMERAS", {})

        for camera_id, camera_info in cameras.items():
            socketio.emit("rtsp_status", {
                "camera_id": camera_id,
                "status": AiStreamService.get_status(camera_id),
                "camera_name": camera_info.get("name", camera_id)
            })

    @socketio.on("disconnect")
    def handle_disconnect():
        """
        소켓 연결 해제 시 실행
        """
        print("[SOCKET] client disconnected")

    @socketio.on("set_detection_target")
    def handle_target(data):
        """
        카메라별 감시 대상(target) 설정 이벤트

        기대 payload 예:
        {
            "camera_id": "cam1",
            "target": "person"
        }
        """
        camera_id = (data or {}).get("camera_id", "")
        target = (data or {}).get("target", "")

        if not camera_id:
            print("[SOCKET] set_detection_target ignored: missing camera_id")
            return

        AiStreamService.set_target(camera_id, target)

    @socketio.on("start_rtsp_stream")
    def handle_start_rtsp(data):
        """
        카메라별 RTSP 시작 이벤트

        기대 payload 예:
        {
            "camera_id": "cam1"
        }
        """
        camera_id = (data or {}).get("camera_id", "")

        cameras = app.config.get("RTSP_CAMERAS", {})
        camera_info = cameras.get(camera_id)

        if not camera_info:
            print(f"[SOCKET] unknown camera_id: {camera_id}")
            return

        if not camera_info.get("enabled", False):
            print(f"[SOCKET] camera disabled: {camera_id}")
            return

        if AiStreamService.is_running(camera_id):
            print(f"[AI] {camera_id} already running")
            return

        camera_name = camera_info.get("name", camera_id)
        rtsp_url = camera_info.get("url", "")

        run_ai_logic = build_run_ai_logic(camera_id, camera_name, rtsp_url)
        socketio.start_background_task(run_ai_logic)

    @socketio.on("stop_rtsp_stream")
    def handle_stop_rtsp(data):
        """
        카메라별 RTSP 종료 이벤트

        기대 payload 예:
        {
            "camera_id": "cam1"
        }
        """
        camera_id = (data or {}).get("camera_id", "")

        if not camera_id:
            print("[SOCKET] stop_rtsp_stream ignored: missing camera_id")
            return

        AiStreamService.request_stop(camera_id)