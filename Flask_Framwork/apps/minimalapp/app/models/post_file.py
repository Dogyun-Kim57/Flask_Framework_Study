from datetime import datetime

from app.extensions import db


class PostFile(db.Model):
    __tablename__ = "post_files"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", name="fk_post_file_post_id"),
        nullable=False
    )

    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    post = db.relationship("Post", back_populates="files")

    def __repr__(self):
        return f"<PostFile {self.id} {self.original_name}>"