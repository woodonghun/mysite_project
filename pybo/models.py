"""
    장고 셸 익히기
    python manage.py shell
    from pybo.models import Question,Answer

    생성 -> 순서대로 진행
    from django.utils import timezone
    q = Question(subject= '', content='', create_date=timezone.now())
    q.save() # save 해야 저장됨
    q.id # 데이터가 생성할 때마다 1씩증가

    조회 -> 각각의 기능
    Question.objects.all()
    Question.objects.filter(id=1)
    Question.objects.get(id=1) => id 값으로 찾을 수 있음
    Question.objects.filter(subject__contains='장고') => 문자열 조회

    수정 -> 순서대로 진행
    Q = Question.objects.get(id=2)
    q.subject = '~'
    q.save()

    삭제 -> 순서대로 진행
    q = Question.objects.get(id=1)
    q.delete()

    Answer 작성 -> 순서대로 진행
    q = Question.objects.get(id=2)
    a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=timezone.now())
    a.save()
    a.id # 마찬가지로 데이터가 생성할 때마나 1씩증가
    질문과 연결된 답변 찾기
    q.answer_set.all()

    todo makemigrations 와 migrate 는 결국 database 에 model 을 적용하는 것을 의미
    todo makemigrations : migrations 코드 생성, migrate : migrations 코드를 데이터베이스에 적용
"""
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
        models.CASCADE 는 유지보수가 어렵다. 만약 user 을 삭제하면 연관되어있는 모든 값들을 지우는데 언제 어디서 지워졌는지 파악하기 어려움. log 를 남기기 어렵다.
        직접 하나씩 지우는 경우는 정확하게 지우기 어렵다.(model.delete()). 언제 어디서 지운지 로그를 남길순 있지만 만약 100개가 넘는 곳에서 지우거나,
        하나씩 지우게 되면 데이터베이스의 통신간 부하가 일어나고, 지워야 할곳에서 코딩실수로 인해 지우지 않고 넘어가 오류가 발생할 수 있다.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델 불러와 회원 가입시 데이터 저장한 계정이 삭제되면 이 계정이 작정한 질문들을 모두 삭제

    # null=True 는 데이터베이스에서 modify_date 칼럼에 null 을 허용한다는 의미이며,
    # blank=True 는 form.is_valid()를 통한 입력 데이터 검증 시 값이 없어도 된다는 의미
    # json 으로 사용하면 form 은 사용하지 않을텐데 검증은 어떻게?
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정된 시간.
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        """
            메서드만 추가될 경우 makemigrations 와 migrate 를 수행 할 필요가 없음. => 모델의 속성이 변경했을때만 수행.
            __str__ => id 값 대신 제목을 표시할 수 있음
            
        """
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
