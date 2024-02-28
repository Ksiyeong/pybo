from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import PostsForm
from django.utils import timezone
from django.contrib import messages
from ..models import Posts



@login_required(login_url='common:login')
def posts_create(request):
    if request.method == 'POST': # POST 요청이면
        form = PostsForm(request.POST) # 다이어리폼에 요청내용을 담는다
        if form.is_valid(): # 폼이 유효한지 검사한다
            posts = form.save(commit=False) # 다이어리라는 변수에 임시저장
            posts.author = request.user # author 값에 로그인중인 유저정보를 담는다
            posts.create_date = timezone.now() # 현재시간 추가
            posts.save() # 최종 저장
            return redirect('/')
    else:
        form = PostsForm()
    context = {'form' : form}
    return render(request, 'main/posts_form.html', context)


@login_required(login_url='common:login')
def posts_modify(request, posts_id):
    posts = get_object_or_404(Posts, pk=posts_id)
    if request.user != posts.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', posts_id=posts.id)
    if request.method == 'POST':
        form = PostsForm(request.POST, instance=posts)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.modify_date = timezone.now()
            posts.save()
            return redirect('main:detail', posts_id=posts.id)
    else:
        form = PostsForm(instance=posts)
    context = {'form': form}
    return render(request, 'main/posts_form.html', context)


@login_required(login_url='common:login')
def posts_delete(request, posts_id):
    posts = get_object_or_404(Posts, pk=posts_id)
    if request.user != posts.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', posts_id=posts.id)
    posts.delete()
    return redirect('index')


@login_required(login_url='common:login')
def posts_vote(request, posts_id):
    posts = get_object_or_404(Posts, pk=posts_id)
    if posts.voter.filter(id=request.user.id).exists():
        posts.voter.remove(request.user)
    else:
        posts.voter.add(request.user)
    return redirect('main:detail', posts_id=posts.id)