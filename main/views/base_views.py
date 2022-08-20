from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from ..models import Posts
from django.db.models import Q, Count



def index(request, category=None):
    page = request.GET.get('page', '1') # 페이지를 읽어온다. 없을경우 1을 뱉는다 ?page =
    kw = request.GET.get('kw', '') # 검색어

    if category == 'freeboard':
        posts_list = Posts.objects.filter(category_id=1).order_by('-create_date')
    elif category == 'diary':
        posts_list = Posts.objects.filter(category_id=2).order_by('-create_date')
    elif category == 'QnA':
        posts_list = Posts.objects.filter(category_id=3).order_by('-create_date')
    else:
        posts_list = Posts.objects.order_by('-create_date')

    if kw:
        posts_list = posts_list.filter( # icontains 대소문자 구분없음, 있음은 contains
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(reply__content__icontains=kw) | # 댓글 내용
            Q(reply__author__username__icontains=kw) | # 댓글 작성자
            Q(author__username__icontains=kw) # 일기 작성자
        ).distinct() # 중복제거
    paginator = Paginator(posts_list, 10) # 한페이지에 보여줄 페이지 갯수 10
    page_obj = paginator.get_page(page) # 페이지 오브젝트에 담아서 보여줌
    context = {'category': category, 'posts_list': page_obj, 'page': page, 'kw': kw}

    return render(request, 'main/posts_list.html', context)


def detail(request, posts_id):
    posts = get_object_or_404(Posts, pk=posts_id)

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', 'first') # 정렬방법

    if kw == 'voter': # 추천순
        paginator = Paginator(posts.reply_set.all().annotate(num_votes=Count('voter')).order_by('-num_votes'), 10)
    elif kw == 'latest': # 최신순
        paginator = Paginator(posts.reply_set.all().order_by('-id'), 10)
    else: # 등록순
        paginator = Paginator(posts.reply_set.all(), 10)

    page_obj = paginator.get_page(page)

    context = {'posts': posts, 'reply_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'main/posts_detail.html', context)