from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer


def index(request):
    """
        order_by는 조회 결과를 정렬하는 함수이다. order_by('-create_date')는 작성일시 역순으로 정렬하라는 의미이다. - 기호가 붙어 있으면 역방향, 없으면 순방향 정렬을 의미한다.

        ORM (Object-Relational Mapping) => Django Class 와 Database Data 를 연결 해주는 것 즉 Question.objects 에서 objects 가 연결해주는 역할을 한다.

        Question.object => Question = Django Class// objects = ORM

        Question_list => QuerySet, 리스트와 구조는 같지만 파이썬 기본 자료구조가 아니라 변환을 해야함.

    """
    question_list = Question.objects.order_by('-create_date')
    print(Question.objects.values(),Question.objects.all())
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 없는 데이터를 요청 할 경우 500 페이지 대신 404 페이지를 출력.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    """아래의 answer_create 와 동일한 기능 수행"""
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id=question.id)

# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     return redirect('pybo:detail', question_id=question.id)
