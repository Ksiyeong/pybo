from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import ReplyForm
from ..models import Diary, Reply



@login_required(login_url='common:login')
def reply_create(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.create_date = timezone.now()
            reply.diary = diary
            reply.save()
            return redirect('main:detail', diary_id=diary.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'diary': diary, 'form': form}
    return render(request, 'main/diary_detail.html', context)


@login_required(login_url='common:login')
def reply_modify(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', diary_id=reply.diary.id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('main:detail', diary_id=reply.diary.id)
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
    return redirect('main:detail', diary_id=reply.diary.id)