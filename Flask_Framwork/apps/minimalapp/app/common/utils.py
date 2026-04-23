def clean_text(value):
    """
    문자열 정리 유틸 함수

    - None이 들어오면 빈 문자열로 처리
    - 앞뒤 공백 제거

    예:
    "  hello  " -> "hello"
    None -> ""
    """
    return (value or "").strip()