import os

BASE_DIR = os.path.dirname(__file__)
# __file__ : C:\projects\myproject\config.py
# os.path.dirname(__file__) = BASE_DIR : # C:\projects\myproject


# 데이터베이스 접속 주소
# 'sqlite:///{C:\projects\myproject\pybo.db}'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

# SQLAlchemy의 이벤트를 처리하는 옵션(수정 추적 시스템을 비활성화)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-WTF를 사용하려면 플라스크의 환경변수 SECRET_KEY가 필요하다. / 폼으로 전송되는 데이터의 필수 여부, 길이, 형식 등을 더 쉽게 검증
SECRET_KEY = "dev"