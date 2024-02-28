from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import ReplyForm
from ..models import Posts, Reply
from math import ceil # 소수점올림 -> 페이지 구하려고



@login_required(login_url='common:login')
def reply_create(request, posts_id):
    posts = get_object_or_404(Posts, pk=posts_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.create_date = timezone.now()
            reply.posts = posts
            reply.save()
            # return redirect('{}?page=0#reply_{}'.format(resolve_url('main:detail', posts_id=posts.id), reply.id)) # 앵커 + ?page=-1 마지막페이지
            return redirect(resolve_url('main:detail', posts_id=posts.id) + '?page=0#reply_' + str(reply.id))
            # main/posts_id + ?page=0#reply_ + reply.id
            # 리졸브로 만든 주소와 받아온 댓글번호 사이에 포멧함수로 끼워넣음 -> 리디렉트
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'posts': posts, 'form': form}
    return render(request, 'main/posts_detail.html', context)


@login_required(login_url='common:login')
def reply_modify(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', posts_id=reply.posts.id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            page = ceil((list(reply.posts.reply_set.all()).index(reply)+1)/10)
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('{}?page={}#reply_{}'.format(
                resolve_url('main:detail', posts_id=reply.posts.id),
                page,
                reply.id
            ))
    else:
        form = ReplyForm(instance=reply)
    context = {'reply': reply, 'form': form}

    return render(request, 'main/reply_form.html', context)


@login_required(login_url='common:login')
def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages.error(request, '권한이 없습니다.')
    else:
        reply.delete()
    return redirect('main:detail', posts_id=reply.posts.id)


@login_required(login_url='common:login')
def reply_vote(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    page = ceil((list(reply.posts.reply_set.all()).index(reply)+1)/10)
    if reply.voter.filter(id=request.user.id).exists():
        reply.voter.remove(request.user)
    else:
        reply.voter.add(request.user)
    return redirect('{}?page={}#reply_{}'.format(
                resolve_url('main:detail', posts_id=reply.posts.id),
                page,
                reply.id
            ))