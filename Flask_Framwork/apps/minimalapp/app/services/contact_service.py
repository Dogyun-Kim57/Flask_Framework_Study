from app.repositories.contact_repository import ContactRepository


class ContactService:
    @staticmethod
    def create_contact(name, email, description):
        name = name.strip()
        email = email.strip()
        description = description.strip()

        if not name:
            raise ValueError("이름은 필수입니다.")

        if not email:
            raise ValueError("이메일은 필수입니다.")

        if not description:
            raise ValueError("문의내용은 필수입니다.")

        return ContactRepository.save(
            name=name,
            email=email,
            description=description
        )