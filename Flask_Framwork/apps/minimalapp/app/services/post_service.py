import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from app.common.exceptions import ValidationError
from app.common.utils import clean_text
from app.repositories.post_file_repository import PostFileRepository
from app.repositories.post_repository import PostRepository


class PostService:
    @staticmethod
    def allowed_file(filename):
        if "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[1].lower()
        return ext in current_app.config["ALLOWED_EXTENSIONS"]

    @staticmethod
    def create_post(user_id, title, content, files):
        title = clean_text(title)
        content = clean_text(content)

        if not user_id:
            raise ValidationError("로그인 후 게시글을 작성할 수 있습니다.")
        if not title:
            raise ValidationError("제목은 필수입니다.")
        if not content:
            raise ValidationError("내용은 필수입니다.")

        post = PostRepository.save(
            user_id=user_id,
            title=title,
            content=content
        )

        PostService._save_files(post.id, files)
        return post

    @staticmethod
    def update_post(post, title, content, files):
        title = clean_text(title)
        content = clean_text(content)

        if not title:
            raise ValidationError("제목은 필수입니다.")
        if not content:
            raise ValidationError("내용은 필수입니다.")

        PostRepository.update(post, title, content)
        PostService._save_files(post.id, files)
        return post

    @staticmethod
    def _save_files(post_id, files):
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        for file in files:
            if not file or not file.filename:
                continue

            if not PostService.allowed_file(file.filename):
                raise ValidationError(f"허용되지 않는 파일 형식입니다: {file.filename}")

            original_name = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex}_{original_name}"
            full_path = os.path.join(upload_folder, unique_name)

            file.save(full_path)
            file_size = os.path.getsize(full_path)

            PostFileRepository.save(
                post_id=post_id,
                original_name=original_name,
                stored_name=unique_name,
                file_path=full_path,
                file_size=file_size
            )

    @staticmethod
    def search_posts(keyword="", sort="latest", my_only=False, user_id=None, page=1, per_page=5):
        return PostRepository.search_paginated(
            keyword=keyword,
            sort=sort,
            my_only=my_only,
            user_id=user_id,
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_post_detail(post_id):
        return PostRepository.find_by_id_with_user_and_files(post_id)

    @staticmethod
    def delete_post(post):
        for file_obj in post.files:
            if os.path.exists(file_obj.file_path):
                os.remove(file_obj.file_path)

        PostRepository.delete(post)

    @staticmethod
    def delete_file(file_obj):
        if os.path.exists(file_obj.file_path):
            os.remove(file_obj.file_path)

        PostFileRepository.delete(file_obj)