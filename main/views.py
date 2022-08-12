from django.shortcuts import render, get_object_or_404, redirect
from .models import Diary
from django.utils import timezone
from .forms import DiaryForm, ReplyForm
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required



def index(request):
    page = request.GET.get('page', '1') # 페이지를 읽어온다. 없을경우 1을 뱉는다 ?page =
    diary_list = Diary.objects.order_by('-create_date')
    paginator = Paginator(diary_list, 10) # 한페이지에 보여줄 페이지 갯수 10
    page_obj = paginator.get_page(page) # 페이지 오브젝트에 담아서 보여줌
    context = {'diary_list' : page_obj}
    return render(request, 'main/diary_list.html', context)


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


def detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    context = {'diary' : diary}
    return render(request, 'main/diary_detail.html', context)


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