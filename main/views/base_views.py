from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from ..models import Diary
from django.db.models import Q



def index(request):
    page = request.GET.get('page', '1') # 페이지를 읽어온다. 없을경우 1을 뱉는다 ?page =
    kw = request.GET.get('kw', '') # 검색어
    diary_list = Diary.objects.order_by('-create_date')
    if kw:
        diary_list = diary_list.filter( # icontains 대소문자 구분없음, 있음은 contains
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(reply__content__icontains=kw) | # 댓글 내용
            Q(reply__author__username__icontains=kw) | # 댓글 작성자
            Q(author__username__icontains=kw) # 일기 작성자
        ).distinct() # 중복제거
    paginator = Paginator(diary_list, 10) # 한페이지에 보여줄 페이지 갯수 10
    page_obj = paginator.get_page(page) # 페이지 오브젝트에 담아서 보여줌
    context = {'diary_list' : page_obj, 'page': page, 'kw': kw}
    return render(request, 'main/diary_list.html', context)


def detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)

    page = request.GET.get('page', '1')
    paginator = Paginator(diary.reply_set.all(), 10)
    page_obj = paginator.get_page(page)

    context = {'diary': diary, 'reply_list': page_obj, 'page': page}
    return render(request, 'main/diary_detail.html', context)