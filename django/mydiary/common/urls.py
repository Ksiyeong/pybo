from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('userdetail/<int:user_id>/', views.userdetail, name='userdetail'),
    path('userdetail/profile_modify/<int:user_id>/', views.profile_modify, name='profile_modify'),
    path('userdetail/profile_delete/<int:user_id>/', views.profile_delete, name='profile_delete'),
]


handler404 = 'common.views.page_not_found'