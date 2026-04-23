# 공통 유틸, 예외, repository import
from app.common.utils import clean_text
from app.common.exceptions import ValidationError
from app.repositories.contact_repository import ContactRepository


class ContactService:
    """
    문의 등록 관련 비즈니스 로직 처리 클래스
    """

    @staticmethod
    def create_contact(user_id, name, email, description):
        """
        문의 등록 처리

        순서:
        1. 입력값 정리
        2. 사용자명 검증
        3. 이메일 검증
        4. 문의내용 검증
        5. DB 저장
        """

        # 공백 제거
        name = clean_text(name)
        email = clean_text(email)
        description = clean_text(description)

        # 사용자명 검증
        if not name:
            raise ValidationError("▶ 사용자명은 필수입니다.")

        # 이메일 필수 검증
        if not email:
            raise ValidationError("▶ 메일 주소는 필수입니다.")

        # 이메일 형식 검증
        # 아주 간단한 1차 검증
        if "@" not in email or "." not in email:
            raise ValidationError("▶ 메일 주소의 형식으로 입력해주세요.")

        # 문의 내용 검증
        if not description:
            raise ValidationError("▶ 문의 내용은 필수입니다.")

        # DB 저장
        return ContactRepository.save(
            user_id=user_id,
            name=name,
            email=email,
            description=description
        )