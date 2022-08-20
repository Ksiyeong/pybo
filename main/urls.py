from django.urls import path
from .views import base_views, posts_views, reply_views


app_name = 'main'

urlpatterns = [
    path('<str:category>/', base_views.index, name='index'),
    path('detail/<int:posts_id>/', base_views.detail, name='detail'),
    
    path('posts/create/', posts_views.posts_create, name='posts_create'),
    path('posts/modify/<int:posts_id>/', posts_views.posts_modify, name='posts_modify'),
    path('posts/delete/<int:posts_id>/', posts_views.posts_delete, name='posts_delete'),
    path('posts/vote/<int:posts_id>/', posts_views.posts_vote, name='posts_vote'),

    path('reply/create/<int:posts_id>/', reply_views.reply_create, name='reply_create'),
    path('reply/modify/<int:reply_id>/', reply_views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', reply_views.reply_delete, name='reply_delete'),
    path('reply/vote/<int:reply_id>/', reply_views.reply_vote, name='reply_vote'),
]