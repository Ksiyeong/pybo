from multiprocessing import context
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth.models import User
from .models import Profile
# from django.contrib.auth import authenticate, login



def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            Profile.objects.create(user_id=user.id)
            return redirect('common:login')
            # # 로그인 후 자동으로 로그인 되기를 원한다면
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # login(request, user)  # 로그인
            # return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def userdetail(request, user_id):
    
    context = {}
    return render(request, 'common/userdetail.html')