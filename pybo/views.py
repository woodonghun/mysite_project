from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


def index(request):
    """
        order_by는 조회 결과를 정렬하는 함수이다. order_by('-create_date')는 작성일시 역순으로 정렬하라는 의미이다. - 기호가 붙어 있으면 역방향, 없으면 순방향 정렬을 의미한다.

        ORM (Object-Relational Mapping) => Django Class 와 Database Data 를 연결 해주는 것 즉 Question.objects 에서 objects 가 연결해주는 역할을 한다.

        Question.object => Question = Django Class// objects = ORM

        Question_list => QuerySet, 리스트와 구조는 같지만 파이썬 기본 자료구조가 아니라 변환을 해야함. 리스트의 안의 타입은 dict
    """
    page = request.GET.get('page', '1')  # Get 으로 요청이 왔을 때 default 1 페이지 get('page', '1')에서 get 은 dict 의 key 값을 불러오는 함수, ('key', '존재하지 않으면 출력할 값 ) 을 의미

    question_list = Question.objects.order_by('-create_date')  # info 중요함 object 와 출력의 기능을 잊지 말것
    # print(Question.objects.values()[0].__class__, Question.objects.all(), question_list)

    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여주기
    print(len(question_list))
    print(type(paginator))
    page_obj = paginator.get_page(page)  # 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하게 됨.
    print(paginator.count, paginator.num_pages, paginator.page_range, type(page_obj))
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 없는 데이터를 요청 할 경우 500 페이지 대신 404 페이지를 출력. pk => primary key
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    """아래의 answer_create 와 동일한 기능 수행"""
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # 폼이 유효하다면
            # """ form.save() 로만 할 경우 form 에는 create_date 의 값이 없어서 오류가 남."""
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴. // commit=False 데이터베이스에 저장 안함.
            question.create_date = timezone.now()  # 실제 저장을 위해 작성 일시를 설정.
            question.save()  # 데이터를 실제로 저장.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)

# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     return redirect('pybo:detail', question_id=question.id)
