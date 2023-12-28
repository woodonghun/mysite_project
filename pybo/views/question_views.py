from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')  # 로그아웃 상태에서 질문/답변을 등록하면 자동으로 로그인 화면으로 이동함. // 강제로 로그인 하게함
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        # 어떤 에러가 발생했는지 보여줌 => 폼을 생성할 때 폼의 fileds 가 유효한지 확인이 되고 오류가 있으면 메세지가 자동으로 form.errors 에 생성이 된다.
        error_messages = '\n'.join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
        print(error_messages)
        print(form.errors, form.errors.items(), form.errors.keys(), form.errors.values())

        if form.is_valid():  # 폼이 유효하다면
            # """ form.save() 로만 할 경우 form 에는 create_date 의 값이 없어서 오류가 남."""
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴. // commit=False 데이터베이스에 저장 안함.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()  # 실제 저장을 위해 작성 일시를 설정.
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
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        print('수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)  # instance => question 객체의 데이터를 사용함 // 없으면 빈 form 이 생성됨
        if form.is_valid():
            question = form.save(commit=False)  # commit=False => database 에 저장하지 않음 => modify_date를 같이 저장하기 위해서?
            question.modify_date = timezone.now()
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
