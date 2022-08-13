from django.db import models
from django.contrib.auth.models import User



class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_diary')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_diary')
    def __str__(self):
        return self.subject


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_reply')
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    # null=True : 데이터베이스에서 null을 허용, blanck=True : form_isvalid 에서 값이 없어도 검사를 통과를 허용
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_reply')