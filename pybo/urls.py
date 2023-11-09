from django.urls import path

from . import views

app_name = 'pybo'   # pybo 앱 이외의 다른 앱이 프로젝트에 추가 될 때, 동일한 url 별칭을 사용하지 않기 위한 방법

urlpatterns = [
    path('', views.index, name='index'),    # url 하드코딩을 해결하기 위한 별칭 부여
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create')
]