from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from common.forms import Profile_ModifyForm, UserForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages



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
    userdetail = get_object_or_404(User, pk=user_id)
    posts_list = userdetail.author_posts.all().order_by('-create_date')
    reply_list = userdetail.author_reply.all()

    context = {'userdetail': userdetail, 'posts_list': posts_list, 'reply_list': reply_list}
    return render(request, 'common/userdetail.html', context)


@login_required(login_url='common:login')
def profile_modify(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)
    print(profile.user_id)
    if request.user != profile.user:
        messages.error(request, '권한이 없습니다.')
        return redirect('/')
    if request.method == 'POST':
        form = Profile_ModifyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('common:userdetail', user_id=profile.user_id)
    else:
        form = Profile_ModifyForm(instance=profile)
    context = {'form': form}
    return render(request, 'common/profile_modify.html', context)