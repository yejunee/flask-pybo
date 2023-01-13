#  질문을 등록할 때 사용할 플라스크의 폼(Form)이다.
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email



class QuestionForm(FlaskForm):  #  FlaskForm 클래스를 상속

    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])  # 글자수의 제한이 있는 "제목"의 경우 StringField를 사용
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')]) #  글자수의 제한이 없는 "내용"은 TextAreaField를 사용

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

#('제목': 폼라벨, validators 검증도구 필수항목체크 이메일인지체크
# 예)  validators=[DataRequired(), Email()]  값필수, 이메일형식

# from wtforms import StringField, TextAreaField, EmailField
# from wtforms.validators import Email
# email = EmailField('email', validators=[DataRequired(), Email()])
# <!-- #이메일 입력폼 사용 HTML
# {{ form.email.label }}
# {{ form.email() }} -->


