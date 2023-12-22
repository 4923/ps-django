"""
URL configuration for guestbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from logs import views

app_name = "logs"

urlpatterns = [
    path("admin/", admin.site.urls),
    # [R] 메인페이지, 방명록 목록을 보여줌
    path("", views.read_logs, name="read_logs"),  # views.py/read_logs 함수를 불러옴
    path("<int:pk>/", views.read_log, name="read_log"),  # 상세페이지
    # [C] 생성
    path("write/", views.write, name="write"),  # 생성 폼
    path("create/", views.create, name="create"),  # 생성 (실행)
    # [U] 수정 및 갱신
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/update/", views.update, name="update"),
    # [D] 삭제
    path("<int:pk>/delete", views.delete, name="delete"),
]
