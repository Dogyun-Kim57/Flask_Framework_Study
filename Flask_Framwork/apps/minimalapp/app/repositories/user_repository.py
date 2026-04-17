# DB 세션 사용을 위해 db import
from app.extensions import db

# User 모델 import
from app.models.user import User


class UserRepository:
    @staticmethod
    def save(username, email, password_hash, role="user"):
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_all():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def promote_to_admin(user):
        user.role = "admin"
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()