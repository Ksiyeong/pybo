from django.db import models

# Create your models here.

class Diary(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    def __str__(self):
        return self.subject


class Reply(models.Model):
    subject = models.ForeignKey(Diary, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()