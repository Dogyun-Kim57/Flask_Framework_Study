from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# 개발 단계에서는 threading 모드로 먼저 안정적으로 연결
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")