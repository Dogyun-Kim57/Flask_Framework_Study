from flask import Blueprint, request, abort, send_file

from app.common.auth import login_required, admin_required, get_current_user_id
from app.common.exceptions import ValidationError
from app.common.response import Response
from app.repositories.post_file_repository import PostFileRepository
from app.services.post_service import PostService


post_bp = Blueprint("post", __name__, url_prefix="/posts")


@post_bp.route("")
def post_list():
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword", "", type=str).strip()
    sort = request.args.get("sort", "latest", type=str)
    my_only = request.args.get("my", 0, type=int) == 1

    pagination = PostService.search_posts(
        keyword=keyword,
        sort=sort,
        my_only=my_only,
        user_id=get_current_user_id(),
        page=page,
        per_page=5
    )

    return Response.render(
        "post/list.html",
        posts=pagination.items,
        pagination=pagination,
        keyword=keyword,
        sort=sort,
        my_only=my_only
    )


@post_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        files = request.files.getlist("files")

        try:
            post = PostService.create_post(
                user_id=get_current_user_id(),
                title=title,
                content=content,
                files=files
            )
            return Response.redirect("post.post_detail", post_id=post.id)

        except ValidationError as e:
            return Response.render(
                "post/create.html",
                error=str(e),
                title=title,
                content=content
            )

    return Response.render("post/create.html")


@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    post = PostService.get_post_detail(post_id)
    if not post:
        abort(404)

    return Response.render("post/detail.html", post=post)


@post_bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = PostService.get_post_detail(post_id)
    if not post:
        abort(404)

    if post.user_id != get_current_user_id():
        return Response.redirect("post.post_detail", post_id=post.id)

    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        files = request.files.getlist("files")

        try:
            PostService.update_post(
                post=post,
                title=title,
                content=content,
                files=files
            )
            return Response.redirect("post.post_detail", post_id=post.id)

        except ValidationError as e:
            return Response.render(
                "post/edit.html",
                post=post,
                error=str(e)
            )

    return Response.render("post/edit.html", post=post)


@post_bp.route("/files/<int:file_id>/download")
@login_required
def download_file(file_id):
    file_obj = PostFileRepository.find_by_id(file_id)
    if not file_obj:
        abort(404)

    return send_file(
        file_obj.file_path,
        as_attachment=True,
        download_name=file_obj.original_name
    )


@post_bp.route("/files/<int:file_id>/delete", methods=["POST"])
@login_required
def delete_file(file_id):
    file_obj = PostFileRepository.find_by_id(file_id)
    if not file_obj:
        abort(404)

    post = file_obj.post

    if post.user_id != get_current_user_id():
        return Response.redirect("post.post_detail", post_id=post.id)

    PostService.delete_file(file_obj)
    return Response.redirect("post.edit_post", post_id=post.id)


@post_bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = PostService.get_post_detail(post_id)
    if not post:
        abort(404)

    if post.user_id != get_current_user_id():
        return Response.redirect("post.post_detail", post_id=post.id)

    PostService.delete_post(post)
    return Response.redirect("post.post_list")


@post_bp.route("/admin")
@admin_required
def admin_post_list():
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword", "", type=str).strip()
    sort = request.args.get("sort", "latest", type=str)

    pagination = PostService.search_posts(
        keyword=keyword,
        sort=sort,
        my_only=False,
        user_id=None,
        page=page,
        per_page=10
    )

    return Response.render(
        "post/admin_list.html",
        posts=pagination.items,
        pagination=pagination,
        keyword=keyword,
        sort=sort
    )


@post_bp.route("/admin/<int:post_id>/delete", methods=["POST"])
@admin_required
def admin_delete_post(post_id):
    post = PostService.get_post_detail(post_id)
    if not post:
        abort(404)

    PostService.delete_post(post)
    return Response.redirect("post.admin_post_list")