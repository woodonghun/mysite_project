from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():  # forms.py 에서 is_valid 함수에 대해 설명됨.
            form.save()  # database 에 저장

            # form.cleaned_data 자체가 dict => 유효성 검사를 하고 form.cleaned_data 라는 딕셔너리에 저장.
            username = form.cleaned_data.get('username')  # 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')

            # authenticate => database 에 접근.
            user = authenticate(username=username, password=raw_password)  # 사용자 인증 ( 사용자 명과 비밀번호가 정확한지 검증 ) 성공하면 객체 반환, 실패 None
            login(request, user)  # 로그인 (사용자 세션을 생성 ) => 데이터베이스나 캐시등에 저장되어 로그인 상태 유지함

            return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
