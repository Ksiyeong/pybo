from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('feed_upload/', views.feed_upload.as_view()),
    path('reply_upload/', views.reply_upload.as_view()),
    path('like_content/', views.like_content.as_view()),
    path('bookmark_content/', views.bookmark_content.as_view())
]
