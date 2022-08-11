from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:diary_id>/', views.detail, name='detail'),
    path('diary/create/', views.diary_create, name='diary_create'),

    path('reply/create/<int:diary_id>/', views.reply_create, name='reply_create'),
]