# Generated by Django 4.1 on 2022-08-13 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_diary_modify_date_reply_modify_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='voter',
            field=models.ManyToManyField(related_name='voter_diary', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reply',
            name='voter',
            field=models.ManyToManyField(related_name='voter_reply', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diary',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_diary', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_reply', to=settings.AUTH_USER_MODEL),
        ),
    ]
