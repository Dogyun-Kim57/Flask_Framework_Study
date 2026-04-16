# 비밀번호 해시 생성/검증용 함수 import
from werkzeug.security import generate_password_hash, check_password_hash

# 공통 유틸, 예외, repository import
from app.common.utils import clean_text
from app.common.exceptions import ValidationError
from app.repositories.user_repository import UserRepository


class AuthService:
    """
    회원가입 / 로그인 관련 비즈니스 로직 처리 클래스
    """

    @staticmethod
    def signup(username, email, password):
        """
        회원가입 처리

        순서:
        1. 입력값 정리
        2. 필수값 검증
        3. 중복 검사
        4. 비밀번호 해시 생성
        5. 회원 저장

        주의:
        - 일반 회원가입은 기본적으로 role='user'로 저장
        - 관리자는 DB에서 직접 변경하거나 추후 관리자 기능으로 승격
        """

        # 입력값 공백 제거
        username = clean_text(username)
        email = clean_text(email)
        password = clean_text(password)

        # 필수값 검증
        if not username or not email or not password:
            raise ValidationError("모든 값을 입력해주세요.")

        # 아이디 중복 검사
        if UserRepository.find_by_username(username):
            raise ValidationError("이미 존재하는 아이디입니다.")

        # 이메일 중복 검사
        if UserRepository.find_by_email(email):
            raise ValidationError("이미 존재하는 이메일입니다.")

        # 비밀번호를 해시로 변환
        password_hash = generate_password_hash(password)

        # 회원 저장
        # 🔥 회원가입 시에는 기본적으로 일반 회원(user)
        return UserRepository.save(
            username=username,
            email=email,
            password_hash=password_hash,
            role="user"
        )

    @staticmethod
    def login(username, password):
        """
        로그인 처리

        순서:
        1. 입력값 정리
        2. 필수값 검증
        3. 사용자 조회
        4. 비밀번호 검증
        5. 성공 시 user 반환

        참고:
        - user 객체 안에 role 정보가 들어있어야
          SessionManager.login(user)에서 관리자/회원 분기 가능
        """

        # 공백 제거
        username = clean_text(username)
        password = clean_text(password)

        # 필수값 검증
        if not username or not password:
            raise ValidationError("아이디와 비밀번호를 입력해주세요.")

        # 회원 조회
        user = UserRepository.find_by_username(username)

        # 회원이 없으면 에러
        if not user:
            raise ValidationError("사용자가 존재하지 않습니다.")

        # 비밀번호 불일치 시 에러
        if not check_password_hash(user.password_hash, password):
            raise ValidationError("비밀번호가 틀렸습니다.")

        # 성공 시 사용자 객체 반환
        return user