# CRUD를 이용한 방명록 만들기

|![](https://github.com/4923/ps-django/assets/60145951/1e723527-cdbe-45e2-a05f-9c7edadfc2fd)|
|:-:|
|[http://4923.pythonanywhere.com/](http://4923.pythonanywhere.com/)|

---

### 기본세팅
1. virtual environment 생성
    ```bash
    # venv 라는 이름으로 생성
    python -m venv venv
    # 실행
    source venv/bin/activate
    ```
2. django 설치
    ```bash
    pip install django
    ```
3. django project 생성
    ```bash
    # 프로젝트 이름 : guestbook
    django-admin startproject guestbook

    # 프로젝트 안에서 작업 시작
    # manage.py가 위치한 경로에서 작업해야한다
    cd guestbook
    ```
4. django app 생성
    ```bash
    # 앱 이름 : logs
    python manage.py startapp logs
    ```
5. 프로젝트에 앱 등록
    ```python
    # guestbook/guestbook/settings.py > INSTALLED_APPS

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "logs",  # 앱 추가
    ]
    ```

### 프로젝트 구성도
| 메인 페이지 | 작성 페이지 | 상세 페이지 | 수정 페이지 | 삭제 기능 |
| :---------: | :---------: | :---------: | :---------: | :-------: |
| ![](https://github.com/4923/ps-django/assets/60145951/ad198116-7962-49ff-9391-43c2da5a4ac7) | ![](https://github.com/4923/ps-django/assets/60145951/66ef37be-1506-4330-83bd-97c79e695a97) | ![](https://github.com/4923/ps-django/assets/60145951/1db48379-ed9e-4e38-b489-4196a4c6a26b) | ![](https://github.com/4923/ps-django/assets/60145951/16133256-30e5-459b-9fec-5039f1d806a9) | ![](https://github.com/4923/ps-django/assets/60145951/650b46db-9bec-43f0-8238-06009abf3196) |
| [Read] `index.html` | [Create] `write.html` | [Read] `details.html` | [Update] `edit.html` | [Delete] `delete` |

### 작업 개요
#### 1. Model 작업
1. `<프로젝트 이름>/<앱 이름>/models.py` 에서 다룰 데이터의 형식을 지정한다.
    ```python
    from django.db import models

    # Create your models here.
    class Log(models.Model):
        # 작성자 이름
        name = models.TextField(max_length=10)
        # 방명록 내용
        contents = models.TextField()
        # 기입 일시 (자동으로 입력: auto_now)
        # 수정일자 : auto_now / 생성일자 : auto_now_add
        datetime = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"[{self.datetime}] {self.name} - {self.contents}"
    ```
2. 데이터베이스에 반영한다.
    ```bash
    # manage.py가 위치한 곳에서
    python manage.py makemigrations
    python manage.py migrate
    ```
#### 2. View 작업
1. `<프로젝트 이름>/<앱 이름>/views.py` 에서 무엇을 보여줄지 정한다.
    - 예시: 메인 페이지와 상세 페이지
    ```python
    
    # 메인페이지: 전부 불러온다.
    def read_logs(request):
        read_logs = Log.objects.all().order_by("datetime").reverse()
        logs = {"logs": read_logs}
        # render(요청을 받았을 때, 어떤 페이지를 보여 줄 것이고, 어떤 데이터를 사용할 것인가)
        return render(request, "index.html", logs)

    # 상세페이지: pk 라는 고유키로 특정 데이터만 불러온다.
    def read_log(request, pk):
        read_log = Log.objects.get(id=pk)
        log = {"log": read_log}
        return render(request, "details.html", log)
    ```
2. 동일하게 본 레포를 참고하여 작성 함수 (`views.write`), 등록 함수 (`views.create`), 수정 함수 (`views.edit`), 갱신 함수 (`views.update`), 삭제 함수 (`views.delete`)를 추가한다.

#### 3. URL 작업
1. `<프로젝트 이름>/<프로젝트 이름>/urls.py` 에서 경로를 지정한다.
    ```python
    from logs import views
    app_name = "logs"

    # [R] 메인페이지, 방명록 목록을 보여준다.
    path("", views.read_logs, name="read_logs"),  # views.py/read_logs 함수를 불러옴
    path("<int:pk>/", views.read_log, name="read_log"),  # 상세페이지
    ```
2. 동일하게 본 레포를 참고하여 생성작업, 수정 및 갱신작업, 삭제 작업 url을 추가한다.

#### 4. Template 작업
1. 보여줄 페이지를 작업한다.
    - views.py 에서 불러오기로 한 페이지 (index.html, details.html) 를 각각 생성해준다.
    - `<프로젝트 이름>/<앱 이름>/templates/base.html` 생성한다.
        ```html
        <!-- 기반이 되는 공통 디자인 -->
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>

            <title>Pungsaeng High School GUESTBOOK</title>
        </head>

        <body>
            <div class="container my-3">
                <br>
                <div class="text-center">
                    <h1 class="display-5" style="padding:3rem 1rem 0rem 1rem">
                        Pungsaeng High School GUESTBOOK
                    </h1>
                <div>
                <br>
                <br>
                {% block contents %}

                {% endblock %}

            <div>
        </body>

        <footer>
            <div class="text-center" style="padding:8rem">
                <small class="text-muted">
                    Copyright © 2023 본인 이름 / PS Codingclass. All rights reserved.
                </small>
            </div>
        </footer>

        </html>
        ```
    - `<프로젝트 이름>/<앱 이름>/templates/파일명.html` 생성한다.
        ```html
        <!-- 예: index.html -->
        
        <!-- 공통 디자인을 불러온다. -->
        {% extends "base.html" %}

        <!-- 공통 디자인에서 확장(extend) 한다. -->
        {% block contents %}
            <table class="table">

            <div class="d-grid d-md-flex justify-content-md-end">
                <a href="{% url 'write' %}" class="btn btn-dark" role="button" style="margin:0rem 0rem 3rem 0rem">
                    작성
                </a>
            <div>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>이름</th>
                        <th>내용</th>
                        <th>작성시간</th>
                    </tr>
                </thead>

                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ forloop.revcounter }}</td>
                        <td>{{log.name}}</td>
                        <td>
                            <a href="{% url 'read_log' log.pk %}" style="text-decoration-line : none; color : black">
                                {{log.contents}}
                            </a>
                        </td>
                        <td>{{log.datetime}}</td>
                    </tr>
                    {% endfor %}
                </tbody>

            </table>

         <!-- 디자인 확장 끝  -->
        {% endblock contents %}
        ```
2. 동일하게 `details.html`, `write.html`, `edit.html` 를 본 레포 참고하여 작성한다.

#### 5. local server 에서 확인
```bash
python manage.py runserver
```

이상 없이 돌아가면 성공

### [추가] pythonanywhere 배포
#### 6. 외부에서 접속할 수 있게 ALLOWED_HOSTS 를 열어준다.
```python
# <프로젝트 이름>/<프로젝트 이름>/settings.py
ALLOWED_HOSTS = ['*']   # [] 빈 리스트에 '*' 추가
```

#### 7. 디버깅 기능은 끈다.
```python
# <프로젝트 이름>/<프로젝트 이름>/settings.py
DEBUG = False   # True에서 변경
```

#### 8. github에 업로드
```bash
# 계정 없을 시 생성
# 프로젝트 폴더 밖에서 (ls 했을 때 프로젝트 이름과 가상환경 이름이 나오는 위치)
ls  # >>> guestbook, venv
git init
git remote add <repo url>
git add .
git commit -m "Add : guestbook files for deploy pythonanywhere"
git push origin main
```

#### 9. pythonanywhere에 업로드
1. 회원가입, 계정명이 주소가 됨에 유의
2. 좌측의 `bash` 클릭
    <img width="1800" alt="image" src="https://github.com/4923/ps-django/assets/60145951/a6ca8c9b-65f3-474c-92e2-e569619db8c6">
3. 열린 창에서 아래 명령어 입력
    ```bash
    git clone <repo url>
    ```
4. WEB APP 생성
    <img width="1798" alt="image" src="https://github.com/4923/ps-django/assets/60145951/da95779c-c1f8-4a76-9170-85b6f65a64de">
5. Manual Configuration 설정으로 생성
6. 아래와 같이 설정
    <img width="767" alt="image" src="https://github.com/4923/ps-django/assets/60145951/c4d44736-6252-4715-a96b-b305028b8769">
    - Source Code, Working directory, static 추가
    - 이 때 
        - 4923 을 `본인의 pythonanywhere` 로 변경
        - ps-django 를 `본인의 github repo 이름` 으로 변경
        - guestbook 을 `본인의 django 프로젝트 이름` 으로 변경
7. WSGI configuration 설정
    - 클릭하면 나오는 창에 아래와 같이 입력
    ```python
    import os
    import sys

    path = '/home/<pythonanywhere 계정 이름>/<github repo 이름>/<django 프로젝트 이름>'
    if path not in sys.path:
    sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = '<django 프로젝트 이름>.settings'

    from django.core.wsgi import get_wsgi_application
    from django.contrib.staticfiles.handlers import StaticFilesHandler

    application = StaticFilesHandler(get_wsgi_application())
    ```
8. 최상단의 초록색 reload 버튼을 누른 후 자신의 주소로 이동 (`<pythonanywhere 계정명>.pythonanywhere.com`)
9. 끝!