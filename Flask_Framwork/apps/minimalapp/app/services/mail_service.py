# Flask-Mail의 Message 객체 import
from flask_mail import Message

# 현재 앱 설정 읽기 위해 current_app 사용
from flask import current_app

# 메일 확장 객체 import
from app.extensions import mail


class MailService:
    """
    메일 발송 전담 서비스

    역할:
    - 문의가 등록되었을 때 관리자 이메일로 문의 내용을 전송
    - 추후 회원가입 환영메일, 비밀번호 재설정 메일 등으로 확장 가능
    """

    @staticmethod
    def send_contact_email(contact):
        """
        문의 내용을 관리자 이메일로 전송

        :param contact: 저장된 Contact 모델 객체
        """

        # 설정파일(config.py / .env)에서 관리자 메일 주소를 읽어온다.
        admin_email = current_app.config.get("ADMIN_EMAIL")

        # 메일 제목 구성
        subject = f"[문의 접수] {contact.name}님의 문의"

        # 메일 본문 구성
        body = f"""
새로운 문의가 접수되었습니다.

[문의자 정보]
- 이름: {contact.name}
- 이메일: {contact.email}
- 사용자 ID: {contact.user_id}

[문의 내용]
{contact.description}

[접수 시간]
{contact.created_at}
        """.strip()

        # Message 객체 생성
        # recipients는 리스트 형태로 전달
        message = Message(
            subject=subject,
            recipients=[admin_email],
            body=body
        )

        # 실제 메일 발송
        mail.send(message)