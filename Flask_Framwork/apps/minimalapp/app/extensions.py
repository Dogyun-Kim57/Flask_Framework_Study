# DB ORM 사용을 위한 SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# DB 마이그레이션 관리용
from flask_migrate import Migrate

# 메일 발송용 Flask-Mail
from flask_mail import Mail

# 프로젝트 전역에서 공통으로 사용할 SQLAlchemy 객체
db = SQLAlchemy()

# 프로젝트 전역에서 공통으로 사용할 Migrate 객체
migrate = Migrate()

# 프로젝트 전역에서 공통으로 사용할 Mail 객체
mail = Mail()