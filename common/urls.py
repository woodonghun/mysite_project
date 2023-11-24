from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

"""
django.contrib.auth -   사용자 관리, 권한 부여, 세션 관리 등 보안과 인증 기능을 제공.
                        1.사용자 관리(User Management): 
                        사용자 생성, 삭제, 변경 등의 기능을 제공.
                        User 모델을 제공하여 기본적인 사용자 정보를 저장. (현재 forms.py 에서 사용)
                        2.인증(Authentication):
                        사용자 로그인, 로그아웃, 세션 관리 등 사용자 인증을 다룸. - 세션 관리 : 웹사이트를 이용하는 동안 일시적으로 정보를 저장 관리 하는것.
                        사용자 인증을 위한 기본적인 뷰와 폼을 제공.
                        3.권한과 그룹(Permissions and Groups):
                        사용자에 대한 권한을 관리하고 그룹화할 수 있는 기능을 제공.
                        사용자에게 특정 권한을 부여하여 특정 기능에 접근을 제한할 수 있습니다.
                        4.비밀번호 관리(Password Management):                    
                        비밀번호 변경, 초기 비밀번호 설정, 비밀번호 재설정 등 비밀번호 관련 기능을 제공.
                        비밀번호 해싱과 같은 보안 관련 기능을 처리. 
"""
app_name = 'common'

urlpatterns = [

    # login, logout 뷰를 따로 만들 필요없이 장고에서 제공하는 django.contrib.auth 앱을 사용
    # 로그인 성공하면 django.contrib.auth 패키지는 디폴트로 /account/profile/ 이라는 url로 이동시켜서 settings에 완료후 url 을 '/' 로 설정함.
    # 로그아웃도 마찬가지로 디폴트로 이동하는 url 이 있어서 따로 설정함.

    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),  # LoginView가 common 디렉터리의 템플릿을 참조
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup')
]
