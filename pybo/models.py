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

"""
from django.db import models


class Question(models.Model):
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        """
            메서드만 추가될 경우 makemigrations 와 migrate 를 수행 할 필요가 없음. => 모델의 속성이 변경했을때만 수행.
            __str__ => id 값 대신 제목을 표시할 수 있음
        """
        return self.question
