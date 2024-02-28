from . import views
from django.urls import path

urlpatterns = [
    path('profile/', views.profile.as_view()),
    path('join/', views.join.as_view()),
    path('login/', views.login.as_view()),
    path('logout/', views.logout.as_view()),
    path('profile/delete_feed', views.delete_feed.as_view()),
    path('profile/update_feed', views.update_feed.as_view()),
    path('profile/verify_pw', views.verify_pw.as_view()),
    path('change_account', views.change_account.as_view()),
    path('delete_account', views.delete_account.as_view())
]