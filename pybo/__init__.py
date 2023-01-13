# pybo.py 와 pybo/__init__.py는 동일한 pybo 모듈이다.
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData # SQLite 데이터베이스에서 사용하는 인덱스 등의 제약 조건 이름은 MetaData 클래스를 사용하여 규칙을 정의해야 한다.

import config

from flaskext.markdown import Markdown


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 애플리케이션 팩토리
def create_app():
    app = Flask(__name__)           # __main__ (pybo모듈)  플라스크 애플리케이션을 생성
    app.config.from_object(config)  # 플라스크앱: Flask 클래스로 만든 객체
                                    # config.py 파일에 작성한 항목을 읽기
    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

 #  db.init_app(app)                # db, migrate와 같은 객체를 create_app 함수 밖에 생성
 #  migrate.init_app(app, db)                                # 해당 객체를 앱에 등록할 때는 create_app 함수에서 init_app 함수를 통해 진행
    from . import models

    # 블루프린트
    from .views import main_views
    from .views import question_views
    from .views import answer_views
    from .views import auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime #  datetime이라는 이름으로  format_datetime 함수 필터를 등록

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code']) # 줄바꿈 / 코드표시
    return app



# 개발 서버 / flask run 실행
# WSGI 서버 / 운영 환경
# 127.0.0.1:5000 현재컴퓨터 아이피 주소 localhost:5000

# @app.route('')는 애너테이션이고 URL 매핑을 만듬.
# 블루프린트(Blueprint)를 사용하여 라우팅 함수를 체계적으로 관리할 수 있다.
#  URL과 함수의 매핑을 관리하기 위해 사용하는 도구(클래스)

""" 
    from flask import Flask
    app = Flask(__name__)
    @app.route('/')             # URL과 플라스크 코드를 매핑하는 플라스크의 데코레이터다. ( 추가 기능을 덧붙일 수 있도록 해주는 함수 )
    def hello_pybo():           # 즉 / URL이 요청되면 플라스크는 hello_pybo 함수를 실행
        return 'Hellp, Pybo!'   # Hello Pybo! 를 출력 
    if __name__ == '__main__':
        app.run()
        
    from flask import Flask
    def create_app():           #  create_app 함수 = 애플리케이션 팩토리
        app = Flask(__name__)
        @app.route('/')
        def hello_pybo():
            return 'Hello, Pybo!'
        return app
        """



