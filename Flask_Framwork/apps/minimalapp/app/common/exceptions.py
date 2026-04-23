class ValidationError(Exception):
    """
    사용자 입력값 검증 실패 시 사용하는 커스텀 예외

    예:
    - 회원가입 시 아이디 누락
    - 문의하기 시 이메일 형식 오류
    """
    pass