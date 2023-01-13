# 화면 구성
# pybo/views/main_views.py

from flask import Blueprint, url_for
from werkzeug.utils import redirect

from pybo.models import Question

# 블루프린트 생성
bp = Blueprint('main', __name__, url_prefix='/')    # main: 블루프린트 별칭, url_for 함수에 사용
                                                    # __name__: main_views모듈
                                                    # 애너테이션 기본 접두어 URL
                                                    # localhost:5000/main/
@bp.route('/hello')              # 라우팅 함수 애너테이션      localhost:5000/
def hello_pybo():
    return 'Hello, pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list')) # redirect: URL로 페이지를 이동
                                               # url_for: 라우팅 함수에 매핑되어 있는 URL을 리턴

# question._list는 question, _list 순서로 해석되어 라우팅 함수를 찾는다.
# question은 등록된 블루프린트 별칭, _list는 블루프린트에 등록된 함수명이다.
# url_for('question._list')는 bp의 프리픽스 URL인 /question/과 /list/가 더해진 /question/list/ URL을 반환

# # @bp.route('/')
# # def index():
# #     question_list = Question.query.order_by(Question.create_date.desc()) # order_by는 조회 결과를 정렬하는 함수 dsec()는 역순 asc()작성일시순
# #     return render_template('question/question_list.html', question_list=question_list) # 템플릿 파일을 화면으로 렌더링 하는 함수
#                                         # http://127.0.0.1:5000/detail/4/
# @bp.route('/detail/<int:question_id>/') # /detail/[[MARK]]2[[/MARK]]/
# def detail(question_id):
#     question = Question.query.get_or_404(question_id)
#     return render_template('question/question_detail.html', question=question)

