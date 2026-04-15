from flask import Blueprint, render_template, request
from app.services.contact_service import ContactService

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        description = request.form.get("description", "")

        try:
            saved_contact = ContactService.create_contact(
                name=name,
                email=email,
                description=description
            )

            return render_template(
                "contact_complete.html",
                username=saved_contact.name,
                email=saved_contact.email,
                description=saved_contact.description
            )
        except ValueError as e:
            return render_template(
                "contact.html",
                error=str(e),
                username=name,
                email=email,
                description=description
            )

    return render_template("contact.html")