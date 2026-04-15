from flask import Flask
from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.contact_routes import contact_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)

    with app.app_context():
        db.create_all()

    return app