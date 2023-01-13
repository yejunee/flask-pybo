# models.py 파일에는 모델 클래스들을 정의하여 사용할 것이다.
# 데이터를 다룰 목적으로 만든 파이썬 클래스

from pybo import db #  db 객체는 __init__.py 파일에서 생성한 SQLAlchemy 클래스의 객체
#pybo로 변경 할 것

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model): # db.Model 클래스를 상속 / Question 모델을 통해 테이블이 생성되면 테이블명은 question이 된다.
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # User 모델을 Question 모델과 연결
    user = db.relationship('User', backref=db.backref('question_set')) #  '1'은 최초로 생성한 User 모델 데이터의 id 값
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set')) # 해당 계정이 추천한 질문 리스트를 구할수 있다.
# user_id 속성은 User 모델을 Question 모델과 연결하기 위한 속성
# user 속성은 Question 모델에서 User 모델을 참조하기 위한 속성

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True) #삭제 연동 설정이다. 즉, ondelete='CASCADE'는 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다는 의미이다.
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) #  모델을 서로 연결할 때에는 위와 같이 db.ForeignKey를 사용
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False) #  답변 모델에서 질문 모델을 참조하기 위해 추가
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # 각 속성은 db.Column으로 생성 / unique=True는 "같은 값을 저장할 수 없다 / null값을 허용하지 않도록 nullable=False
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
    # question_id 속성은 답변을 질문과 연결하기 위해 추가한 속성 / 질문의 id 속성이 필요
    #Answer 모델의 question_id 속성은 question 테이블의 id 컬럼과 연결

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    ################## c https://wikidocs.net/81045
    # 플라스크 셸 실행하기

    # 답변    데이터    저장하기

    # 답변에 연결된 질문 찾기 vs 질문에 달린 답변 찾기