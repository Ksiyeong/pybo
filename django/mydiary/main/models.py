from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name


class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts', null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_posts')

    def __str__(self):
        return self.subject


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_reply')
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    # null=True : 데이터베이스에서 null을 허용, blanck=True : form_isvalid 에서 값이 없어도 검사를 통과를 허용
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_reply')