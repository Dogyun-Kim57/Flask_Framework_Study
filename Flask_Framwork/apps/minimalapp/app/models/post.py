from datetime import datetime

from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_post_user_id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 작성자
    user = db.relationship("User", back_populates="posts")

    # 첨부파일
    files = db.relationship(
        "PostFile",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Post {self.id} {self.title}>"