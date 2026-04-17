# 모델들을 한 곳에서 import 해두면
# 앱 초기화나 마이그레이션 시 모델 인식이 쉬워진다.

from app.models.user import User
from app.models.contact import Contact
from app.models.post import Post
from app.models.post_file import PostFile