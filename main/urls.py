from django.urls import path
from .views import base_views, diary_views, reply_views


app_name = 'main'

urlpatterns = [
    path('<str:category>/', base_views.index, name='index'),
    path('detail/<int:diary_id>/', base_views.detail, name='detail'),
    
    path('diary/create/', diary_views.diary_create, name='diary_create'),
    path('diary/modify/<int:diary_id>/', diary_views.diary_modify, name='diary_modify'),
    path('diary/delete/<int:diary_id>/', diary_views.diary_delete, name='diary_delete'),
    path('diary/vote/<int:diary_id>/', diary_views.diary_vote, name='diary_vote'),

    path('reply/create/<int:diary_id>/', reply_views.reply_create, name='reply_create'),
    path('reply/modify/<int:reply_id>/', reply_views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', reply_views.reply_delete, name='reply_delete'),
    path('reply/vote/<int:reply_id>/', reply_views.reply_vote, name='reply_vote'),
]