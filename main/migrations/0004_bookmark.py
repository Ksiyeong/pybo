# Generated by Django 4.0.6 on 2022-07-29 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.IntegerField()),
                ('User_ID', models.TextField()),
            ],
            options={
                'db_table': 'Bookmark',
            },
        ),
    ]
