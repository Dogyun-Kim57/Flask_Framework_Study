# app 패키지 안에 있는 create_app 함수를 불러온다.
# 이 함수는 Flask 앱 객체를 생성하고 설정까지 마친 뒤 반환한다.
from app import create_app

# 실제 Flask 앱 인스턴스를 생성한다.
app = create_app()

# 이 파일을 직접 실행했을 때만 아래 코드가 동작한다.
if __name__ == "__main__":
    # host="127.0.0.1" : 현재 PC(로컬)에서만 접속 가능
    # port=8000        : 8000번 포트에서 실행
    # debug=True       : 개발용 디버그 모드
    app.run(host="127.0.0.1", port=8000, debug=True)