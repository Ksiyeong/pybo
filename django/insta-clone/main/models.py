from django.db import models

class Feed(models.Model):
    User_ID = models.TextField()
    feed_img = models.TextField()
    feed_content = models.TextField()

    USERNAME_FIELD = 'User_ID'

    class Meta:
        db_table = "Feed"


class Reply(models.Model):
    content_id = models.TextField()
    User_ID = models.TextField()
    reply = models.TextField()

    USERNAME_FIELD = 'reply'

    class Meta:
        db_table = "Reply"


class Like(models.Model):
    content_id = models.IntegerField()
    User_ID = models.TextField()

    USERNAME_FIELD = 'User_ID'

    class Meta:
        db_table = 'Like'

    
class Bookmark(models.Model):
    content_id = models.IntegerField()
    User_ID = models.TextField()

    USERNAME_FIELD = 'User_ID'

    class Meta:
        db_table = 'Bookmark'