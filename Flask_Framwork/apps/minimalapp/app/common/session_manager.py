from flask import session


class SessionManager:
    """
    세션(Session) 관리 전담 클래스

    목적:
    - 로그인/로그아웃 시 session 직접 접근 코드 제거
    - session 구조를 한 곳에서 통일 관리
    - 추후 JWT / Redis 세션 등으로 변경 시 영향 최소화

    현재 구조:
    Flask session 기반
    """

    @staticmethod
    def login(user):
        """
        로그인 성공 시 호출

        역할:
        - 사용자 정보를 session에 저장
        - 이 정보는 브라우저 쿠키(session)에 자동 저장됨

        중요:
        - role 값도 반드시 저장해야
          헤더에서 관리자 / 회원 기능 분기가 가능해진다.
        """

        # 사용자 고유 ID 저장
        session["user_id"] = user.id

        # 화면 표시용 username 저장
        session["username"] = user.username

        # 이메일 저장
        session["user_email"] = user.email

        # 🔥 권한 저장
        # admin / user 구분용
        session["role"] = user.role

    @staticmethod
    def logout():
        """
        로그아웃 처리

        역할:
        - session 전체 제거
        """
        session.clear()

    @staticmethod
    def get_user_id():
        """
        현재 로그인된 사용자 ID 반환
        """
        return session.get("user_id")

    @staticmethod
    def get_username():
        """
        현재 로그인된 사용자 이름 반환
        """
        return session.get("username")

    @staticmethod
    def get_email():
        """
        현재 로그인된 사용자 이메일 반환
        """
        return session.get("user_email")

    @staticmethod
    def get_role():
        """
        현재 로그인된 사용자 권한 반환
        - admin
        - user
        """
        return session.get("role")