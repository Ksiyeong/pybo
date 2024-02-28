from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class User(AbstractBaseUser):
    """
    유저 아이디
    유저 닉네임
    유저 이름
    유저 프로필 사진
    유저 비밀번호
    """
    User_ID = models.TextField(unique=True)
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    profile_image = models.TextField()
    profile_comment = models.TextField(default=None)
    
    USERNAME_FIELD = 'User_ID'

    class Meta:
        db_table = "User"