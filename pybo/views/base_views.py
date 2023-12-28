from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    """
        ORM (Object-Relational Mapping) => Django Class 와 Database Data 를 연결 해주는 것 즉 Question.objects 에서 objects 가 연결해주는 역할을 한다.

        Question.object => Question = Django Class// objects = ORM

        Question_list => QuerySet, 리스트와 구조는 같지만 파이썬 기본 자료구조가 아니라 변환을 해야함. 리스트의 안의 타입은 dict
    """
    page = request.GET.get('page', '1')  # Get 으로 요청이 왔을 때 default 1 페이지 get('page', '1')에서 get 은 dict 의 key 값을 불러오는 함수, ('key', '존재하지 않으면 출력할 값 ) 을 의미
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')  # order_by=> 조회 결과를 정렬, -create_date 에서 - 는 역순 정렬을 의미함.
    # print(Question.objects.values()[0].__class__, Question.objects.all(), question_list)

    """ 
        Q 함수는 논리연산자로 데이터를 조회하기 위해 사용하는 함수이다. 
        & (AND), | (OR), ~ (NOT)
        distinct 는 조회 결과에 중복이 있을 경우 중복을 제거하여 리턴하는 함수.
        POST 가 아닌 GET 방식.
        
        __ 의 의미는 관계를 지정하는데 사용 
        ex) answer__author__username => answer 모델의 author 필드를 통해 연결된 모델의 username 필드
        현재 question 이 없는 이유는 question_list 가 이미 quetion 모델에 접근했기 때문
        
        icontains : 대소문자를 구분하지 않고 포함하는지 확인
        iexact : 대소문자를 구분하지 않고 정확히 일치하는지 확인
        isnull : null 여부를 확인 
        등등 다양한 필터링 옵션을 제공
    """

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__author__username__icontains=kw) |    # 댓글 작성자
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) |  # 답변 글쓴이 검색
            Q(comment__content__icontains=kw)
        ).distinct()    # distinct => 중복제거

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    # print(len(question_list))
    # print(type(paginator))
    page_obj = paginator.get_page(page)  # 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하게 됨.
    # print(paginator.count, paginator.num_pages, paginator.page_range, page_obj.next_page_number())
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 없는 데이터를 요청 할 경우 500 페이지 대신 404 페이지를 출력. pk => primary key
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
