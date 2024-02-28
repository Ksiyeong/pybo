from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model): # 기본 유저모델에 간단하게 추가해서 사용
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=100, default="자기소개 입니다.")
    bloodtype = models.CharField(max_length=20, default="혈액형을 알려주세요.")

    def __str__(self):
        return self.user.username