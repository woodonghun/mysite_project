import mimetypes
import os
import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question
from config import settings


@login_required(login_url='common:login')  # 로그아웃 상태에서 질문/답변을 등록하면 자동으로 로그인 화면으로 이동함. // 강제로 로그인 하게함
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)  # 폼 데이터와 파일 데이터는 따로 처리함.  request.FILES : QueryDict
        # 어떤 에러가 발생했는지 보여줌 => 폼을 생성할 때 폼의 fileds 가 유효한지 확인이 되고 오류가 있으면 메세지가 자동으로 form.errors 에 생성이 된다.
        error_messages = '\n'.join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
        # print(error_messages)
        # print(form.errors, form.errors.items(), form.errors.keys(), form.errors.values())

        if form.is_valid():  # 폼이 유효하다면
            # """ form.save() 로만 할 경우 form 에는 create_date 의 값이 없어서 오류가 남."""
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴. // commit=False 데이터베이스에 저장 안함.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()  # 실제 저장을 위해 작성 일시를 설정.
            if request.FILES:
                if 'file' in request.FILES.keys():
                    question.filename = request.FILES['file'].name
            question.save()  # 데이터를 실제로 저장.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    original_file_tf = False
    original_file = ''
    original_filename = ''

    if question.file:  # 기존에 파일이 존재할 때
        original_file = question.file
        original_filename = question.filename
        original_file_tf = True

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        print('수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=question)  # instance => question 객체의 데이터를 사용함 // 없으면 빈 form 이 생성됨
        if form.is_valid():
            question = form.save(commit=False)  # commit=False => database 에 저장하지 않음 => modify_date를 같이 저장하기 위해서?
            question.modify_date = timezone.now()

            file_check = request.POST.get('file-clear', False)  # 삭제 버튼 ( 취소라고 써있음 )

            if request.FILES:   # 파일 요청
                if 'file' in request.FILES.keys():
                    question.filename = request.FILES['file'].name
                    print('request')
            else:   # 파일 요청 x
                question.file = original_file
                question.filename = original_filename

            if original_file_tf:
                if file_check == 'on':  # 파일을 삭제했을때, ( 삭제 버튼 체크 )
                    os.remove(os.path.join(settings.MEDIA_ROOT, original_file.path))
                    question.file = None
                    question.filename = None
                    print('delete')
                elif original_file.url != question.file.url:  # 파일이 변경되었을때
                    os.remove(os.path.join(settings.MEDIA_ROOT, original_file.path))
                    print('change')

            question.save()  # 데이터를 실제로 저장.
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


# 파일 저장 ( 한글도 가능 )
def question_file_download(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # question.file.url 은 한글일 경우 percent 인코딩이 되어 나온다. // url 로는 특수문자, 한글 등을 사용할수 없어서 변환함.
    # [1:] 부터 한 이유는 제일 앞 / 를 제거하기 위해서 ( % 인코딩 ) - setting.py 에서 /media/ 로 지정
    url = question.file.url[1:]
    print(url)
    # 퍼센트 인코딩된 텍스트를 되돌리기(디코딩) 위해 urllib.parse.unquote로 변환 후 file_url에 저장 => 한글일때 적용됨 ( 한글 적용 )
    file_url = urllib.parse.unquote(url)
    print(file_url)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:  # 바이너리 파일을 읽기 위해 rb 인자 설정

            # utf-8로 인코딩한 파일을 urllib.parse.quote를 통해 퍼센트 인코딩으로 변환
            quote_file_url = urllib.parse.quote(question.filename.encode('utf-8'))  # ( % 인코딩 )

            # content_type=mimetypes.guess_type(file_url)[0] 데이터 타입 추측 // text, image ...
            # fh.read() 파일 읽고 반환
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])

            # Content-Disposition 는 http response body(응답의 body) 에 오는 컨텐츠의 기질/성향을 알려주는 속성
            # attachment : 다운로드 해야함
            # filename*=UTF-8''%s 파일 이름을 utf-8로 인코딩 한것을 나타냄
            # \'\' 는 단순히 작은 따옴표 안에 작은 따옴표를 표현하기 위함. filename*=UTF-8\'\'%s => filename*=UTF-8''%s

            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404  # file_url 에 파일이 없으면 404
