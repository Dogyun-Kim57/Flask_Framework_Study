# Flask의 템플릿 렌더링, 리다이렉트, URL 생성, JSON 응답 기능 import
from flask import render_template, redirect, url_for, jsonify


class Response:
    """
    공통 응답 처리 클래스

    장점:
    - render_template를 직접 반복 호출하지 않아도 됨
    - redirect 패턴을 통일 가능
    - 추후 API 응답도 같은 형식으로 관리 가능
    """

    @staticmethod
    def render(template_name, **context):
        """
        HTML 템플릿 렌더링

        :param template_name: 렌더링할 템플릿 경로
        :param context: 템플릿에 넘길 데이터
        """
        return render_template(template_name, **context)

    @staticmethod
    def redirect(endpoint, **values):
        """
        endpoint 기준 리다이렉트 처리

        예:
        Response.redirect("main.index")
        """
        return redirect(url_for(endpoint, **values))

    @staticmethod
    def json_success(message="success", data=None, status=200):
        """
        성공 JSON 응답 반환

        API 형태가 필요할 때 사용 가능
        """
        payload = {
            "success": True,
            "message": message,
            "data": data
        }
        return jsonify(payload), status

    @staticmethod
    def json_error(message="error", data=None, status=400):
        """
        실패 JSON 응답 반환

        API 에러 응답 형식을 통일할 때 사용 가능
        """
        payload = {
            "success": False,
            "message": message,
            "data": data
        }
        return jsonify(payload), status