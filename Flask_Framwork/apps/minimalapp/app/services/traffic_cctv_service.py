import requests
from flask import current_app


class TrafficCctvService:
    @staticmethod
    def get_cctv_list(
        min_x="126.70",
        max_x="127.20",
        min_y="37.30",
        max_y="37.70",
        road_type="all",
        cctv_type="5"
    ):
        api_key = current_app.config.get("ITS_API_KEY")
        api_url = current_app.config.get("ITS_CCTV_API_URL")

        if not api_key:
            raise ValueError("ITS_API_KEY가 설정되어 있지 않습니다.")

        params = {
            "apiKey": api_key,
            "type": road_type,
            "cctvType": cctv_type,
            "minX": min_x,
            "maxX": max_x,
            "minY": min_y,
            "maxY": max_y,
            "getType": "json",
        }

        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        raw_items = data.get("response", {}).get("data", [])

        result = []

        for item in raw_items:
            cctv_url = item.get("cctvurl") or item.get("url") or ""

            result.append({
                "name": item.get("cctvname", ""),
                "url": cctv_url,
                "format": item.get("cctvformat", ""),
                "type": item.get("cctvtype", ""),
                "resolution": item.get("cctvresolution", ""),
                "road_section_id": item.get("roadsectionid", ""),
                "coordx": item.get("coordx", ""),
                "coordy": item.get("coordy", ""),
                "file_create_time": item.get("filecreatetime", ""),
            })

        return result