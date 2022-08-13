from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:diary_id>/', views.detail, name='detail'),
    path('diary/create/', views.diary_create, name='diary_create'),
    path('diary/modify/<int:diary_id>/', views.diary_modify, name='diary_modify'),
    path('diary/delete/<int:diary_id>/', views.diary_delete, name='diary_delete'),

    path('reply/create/<int:diary_id>/', views.reply_create, name='reply_create'),
    path('reply/modify/<int:reply_id>/', views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', views.reply_delete, name='reply_delete'),
]