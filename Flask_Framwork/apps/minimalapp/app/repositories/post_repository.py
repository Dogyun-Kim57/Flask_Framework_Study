from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.post import Post
from app.models.user import User


class PostRepository:
    @staticmethod
    def save(user_id, title, content):
        post = Post(
            user_id=user_id,
            title=title,
            content=content
        )
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def search_paginated(
        keyword="",
        sort="latest",
        my_only=False,
        user_id=None,
        page=1,
        per_page=5
    ):
        query = (
            Post.query
            .join(User)
            .options(
                joinedload(Post.user),
                joinedload(Post.files)
            )
        )

        if keyword:
            like_keyword = f"%{keyword}%"
            query = query.filter(
                or_(
                    Post.title.like(like_keyword),
                    Post.content.like(like_keyword),
                    User.username.like(like_keyword)
                )
            )

        if my_only and user_id:
            query = query.filter(Post.user_id == user_id)

        if sort == "oldest":
            query = query.order_by(Post.created_at.asc())
        else:
            query = query.order_by(Post.created_at.desc())

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def find_by_id_with_user_and_files(post_id):
        return (
            Post.query
            .options(
                joinedload(Post.user),
                joinedload(Post.files)
            )
            .filter_by(id=post_id)
            .first()
        )

    @staticmethod
    def update(post, title, content):
        post.title = title
        post.content = content
        db.session.commit()
        return post

    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()