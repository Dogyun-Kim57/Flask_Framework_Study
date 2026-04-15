from app.extensions import db
from app.models.contact import Contact


class ContactRepository:
    @staticmethod
    def save(name, email, description):
        contact = Contact(
            name=name,
            email=email,
            description=description
        )
        db.session.add(contact)
        db.session.commit()
        return contact

    @staticmethod
    def find_all():
        return Contact.query.all()

    @staticmethod
    def find_by_id(contact_id):
        return Contact.query.get(contact_id)