from dotenv import load_dotenv

load_dotenv()

# app 패키지 안의 create_app 함수 import
from app import create_app

# socketio 객체 import
from app.extensions import socketio

# Flask app 생성
app = create_app()

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=8000,
        debug=True,
        allow_unsafe_werkzeug=True
    )