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
