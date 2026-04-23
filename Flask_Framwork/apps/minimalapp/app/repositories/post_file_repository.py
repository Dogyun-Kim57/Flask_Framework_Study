from app.extensions import db
from app.models.post_file import PostFile


class PostFileRepository:
    @staticmethod
    def save(post_id, original_name, stored_name, file_path, file_size):
        post_file = PostFile(
            post_id=post_id,
            original_name=original_name,
            stored_name=stored_name,
            file_path=file_path,
            file_size=file_size
        )
        db.session.add(post_file)
        db.session.commit()
        return post_file

    @staticmethod
    def find_by_id(file_id):
        return PostFile.query.get(file_id)

    @staticmethod
    def delete(file_obj):
        db.session.delete(file_obj)
        db.session.commit()