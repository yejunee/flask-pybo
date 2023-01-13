from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth') # 우선 /auth/로 시작하는 URL이 호출되면  auth_views.py 파일의 함수들이 호출
#계정생성
@bp.route('/signup/', methods=('GET', 'POST')) #  POST 방식에는 계정을 저장하고 GET 방식에는 계정 등록 화면을 출력
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # 특정 column 만 select one all  non-iterator 값을 반환
        if not user: # !0 없다면
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else: # 이미 등록된 사용자
            flash('이미 존재하는 사용자입니다.') # 논리 오류 발생 함수

    return render_template('auth/signup.html', form=form)
# print(not 1)

# 로그인
@bp.route('/login/', methods=('GET', 'POST'))
def login(): # login 함수
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit(): # POST방식 로그인 수행
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user: # not 0 = 1 없다면
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): #check_password_hash 함수로 암호화한 후 데이터베이스의 값과 비교
            error = "비밀번호가 올바르지 않습니다."
        if error is None: # 사용자 존재 비밀번호 일치
            session.clear()
            session['user_id'] = user.id # 세션 키에 'user_id'라는 문자열을 저장하고 키에 해당하는 값은 데이터베이스에서 조회한 사용자의 id 값을 저장
            _next = request.args.get('next', '')  # 값이있다면 첫번째인자 없다면 두번째 인자 반환
            # print("**************", request.args.get('next', ''))
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
            return redirect(url_for('main.index'))
        flash(error) #  필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수
    return render_template('auth/login.html', form=form)

@bp.before_app_request # 이 애너테이션이 적용된 함수는 라우팅 함수보다 항상 먼저 실행
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None # g는 플라스크의 컨텍스트 변수  [요청 → 응답] 과정에서 유효 /
    else:
        g.user = User.query.get(user_id) #  session 변수에 user_id값이 있으면 g.user에 저장 g.user에는 User 객체가 저장된다.

# 데코레이터 함수 기존 함수를 감싸는 방법
@bp.route('/logout/')  # 데코레이터
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):  # @login_required def create() = (함수) = views #  함수의 올바른 동작을 보장
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs): # create함수의 인수 question_id
        # print("===================================",type(kwargs))
        # print("+++++++++++++++++++++++++++++++++++",view)
        # print("-----------------------------------", args, kwargs, request.url)
        if g.user is None:
            _next = request.url if request.method == "GET" else request.url # 로그인 후에 원래 가려던 페이지로 다시 찾아갈수 있도록 로그인 페이지에 next 파라미터를 전달했다.
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", _next)
            return redirect(url_for('auth.login', next=_next))
        # print("+++++++++++++++++++++++++++++++++++", args, kwargs, request.url)
        return view(*args, **kwargs)
    return wrapped_view

@bp.route('/delete/', methods=('GET', 'POST'))
@login_required
def delete():
    form = UserCreateForm()
    print("------------------------",form.email)
    return render_template('auth/del.html')

    # user = User.query.get(g.user.id)
    # if g.user != question.user:
    #     flash('삭제권한이 없습니다')
    #     return redirect(url_for('auth.delacc', user_id=user_id))
    # db.session.delete(user)
    # db.session.commit()
    # return redirect(url_for('question._list'))

#계정삭제
@bp.route('/delacc/', methods=('GET', 'POST') )
def delacc():
    flash('계정을 삭제 후 복구 불가능 합니다.')
    user_list = User.query.order_by(User.id.desc())
    form = UserCreateForm()
    return render_template('auth/delacc.html', form=form, user_list=user_list)

# class UserCreateForm(FlaskForm):
#     username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
#     password1 = PasswordField('비밀번호', validators=[
#         DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
#     password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
#     email = EmailField('이메일', validators=[DataRequired(), Email()])