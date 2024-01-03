"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def protected_file(request, path, document_root=None):
    messages.error(request, "접근 불가")
    print(request)
    return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]

# if settings.DEBUG:
#     # 개발 서버로 실행 중 일떄 설정된 곳으로 접근하는 요청을 처리하기 위한 설정 // 미디어 파일을 로컬 pc 에 저장할 수 있고 직접 관리, 접근할 수 있으면 사용하지 않아도 무관함,
#     urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)  # media 경로 추가 // 사용자가 업로드한 파일들을 개발 서버에서 확인할 수 있게 해줌
#     # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # media 경로 추가 // 사용자가 업로드한 파일들을 개발 서버에서 확인할 수 있게 해줌
