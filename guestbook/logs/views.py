from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404  # 추가

# Create your views here.
# 생성한 앱의 모델 추가 (app name: logs, model name: Log)
from logs.models import Log

# UTC가 기본이므로 guestbook/guestbook/settings.py 에서
# TIME_ZONE = 'Asia/Seoul' 추가 (USE_TZ = False 로 변경)
from django.utils import timezone

"""
Read: 방명록 열람 (목록 반환)
Create: 방명록 생성
    - 사용자명, 비밀번호 입력
Update: 방명록 수정
    - 비밀번호 필요
Delete: 방명록 삭제
    - 비밀번호 필요
"""


def read_logs(request):
    read_logs = Log.objects.all().order_by("datetime").reverse()
    logs = {"logs": read_logs}
    return render(request, "index.html", logs)


def read_log(request, pk):
    read_log = Log.objects.get(id=pk)
    log = {"log": read_log}
    return render(request, "details.html", log)


def write(request):
    return render(request, "write.html")


def create(request):
    """
    # guestbook/logs/models.py
    class Logs(models.Model):
        # 작성자 이름
        name = models.TextField()
        # 방명록 내용
        contents = models.TextField()
        # 기입 일시 (자동으로 입력: auto_now)
        # 수정일자 : auto_now / 생성일자 : auto_now_add
        datetime = models.DateTimeField(auto_now=True)
    """
    new_log = Log()
    new_log.name = request.POST["name"]
    new_log.contents = request.POST["contents"]
    # datetime은 자동으로 추가되므로 POST입력 받지 않아도 됨
    new_log.save()

    return redirect("read_log", pk=new_log.pk)


def edit(request, pk):
    """write(create)와 유사, 기존 데이터를 불러와 update 함수로 덮어씌운다."""
    read_log = Log.objects.get(id=pk)  # 원래 저장된 데이터를 불러온다
    log = {"log": read_log}
    return render(request, "edit.html", log)


def update(request, pk):
    # 올바르지 않은 고유번호 primary key 일 경우 404 에러 반환
    log = get_object_or_404(Log, pk=pk)
    # 작성자 이름, 비밀번호는 수정 불가
    # 내용만 수정하도록 변경
    log.contents = request.POST["contents"]

    # 아래 라인 추가
    # from django.utils import timezone
    log.datetime = timezone.now()
    log.save()

    return redirect("read_log", pk=pk)


def delete(request, pk):
    log = Log.objects.get(id=pk)
    log.delete()
    return redirect("read_logs")
