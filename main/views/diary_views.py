from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import DiaryForm
from django.utils import timezone
from django.contrib import messages
from ..models import Diary



@login_required(login_url='common:login')
def diary_create(request):
    if request.method == 'POST': # POST 요청이면
        form = DiaryForm(request.POST) # 다이어리폼에 요청내용을 담는다
        if form.is_valid(): # 폼이 유효한지 검사한다
            diary = form.save(commit=False) # 다이어리라는 변수에 임시저장
            diary.author = request.user # author 값에 로그인중인 유저정보를 담는다
            diary.create_date = timezone.now() # 현재시간 추가
            diary.save() # 최종 저장
            return redirect('main:index')
    else:
        form = DiaryForm()
    context = {'form' : form}
    return render(request, 'main/diary_form.html', context)


@login_required(login_url='common:login')
def diary_modify(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', diary_id=diary.id)
    if request.method == 'POST':
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.modify_date = timezone.now()
            diary.save()
            return redirect('main:detail', diary_id=diary.id)
    else:
        form = DiaryForm(instance=diary)
    context = {'form': form}
    return render(request, 'main/diary_form.html', context)


@login_required(login_url='common:login')
def diary_delete(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('main:detail', diary_id=diary.id)
    diary.delete()
    return redirect('index')


@login_required(login_url='common:login')
def diary_vote(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    diary.voter.add(request.user)
    return redirect('main:detail', diary_id=diary.id)