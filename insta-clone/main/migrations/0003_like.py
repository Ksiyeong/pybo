# Generated by Django 4.0.6 on 2022-07-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.IntegerField()),
                ('User_ID', models.TextField()),
            ],
            options={
                'db_table': 'Like',
            },
        ),
    ]