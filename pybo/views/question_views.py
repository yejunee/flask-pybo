from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from.. import db
from pybo.models import Question, Answer, User
from pybo.forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question') # 이름,

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        print(search)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# 질문등록하기
@bp.route('/create/', methods=('GET', 'POST')) #  GET과 POST 방식을 모두 처리할수 있도록 라우팅 애너테이션에 methods 속성을 추가
@login_required
def create(): # <질문 등록하기> 기본 get 방식 post는 <저장하기> 버튼

    form = QuestionForm()  # request.method: create 함수로 요청된 전송 방식
    if request.method == 'POST' and form.validate_on_submit(): # QuestionForm 클래스의 각 속성에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index')) # 페이지 위?
    return render_template('question/question_form.html', form=form) # 템플릿에 전달하는 QuestionForm의 객체(form)는 템플릿에서 라벨이나 입력폼 등을 만들때 필요

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required # 애너테이션
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다') # flash 함수는 강제로 오류를 발생시키는 함수로, 로직에 오류가 있을 경우 사용한다.
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청 수정 화면에서 데이터를 수정한 다음 <저장하기> 버튼을 눌렀을 경우
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question) # form 변수에 들어 있는 데이터(화면에서 입력한 데이터)를 question 객체에 업데이트 하는 역할
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청 < 질문수정 > 버튼을 눌렀을 때
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))








############################################################################################################

# render_template 함수는 템플릿 파일을 화면으로 렌더링 하는 함수이다.
# 조회한 질문 목록 데이터를 render_template 함수의 파라미터로 전달하면 템플릿에서 해당 데이터로 화면을 구성할수 있다.

# http://localhost:5000/question/list/?question_id=4
# < li > < a href = "{{ url_for('question.list', question_id=question.id) }}" > {{question.subject}} < / a > < / li >

# http://localhost:5000/question/detail/4/
# < li > < a href = "{{ url_for('question.detail', question_id=question.id) }}" > {{question.subject}} < / a > < / li >