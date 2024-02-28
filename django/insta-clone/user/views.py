from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from main.models import Feed, Like, Bookmark, Reply
from django.contrib.auth.hashers import make_password
import os
from uuid import uuid4
from 인스타클론.settings import MEDIA_ROOT


class profile(APIView):
    def get(self, request):
        user = User.objects.filter(User_ID=request.session.get('User_ID')).first()

        if user == None:
            return render(request, 'user/login.html')
        
        btn = request.GET.get('btn')
        if btn == None:
            now_searchname = ''
            feed_list = Feed.objects.filter(User_ID=user.User_ID).order_by('-id')
        elif btn == 'like':
            now_searchname = 'like'
            like_list = Like.objects.filter(User_ID=user.User_ID).order_by('-id')
            feed_list = []
            for like in like_list:
                feed_list.append({
                    'feed_img' : Feed.objects.filter(id=like.content_id).first().feed_img,
                    'id' : Feed.objects.filter(id=like.content_id).first().id
                })
        elif btn == 'bookmark':
            now_searchname = 'bookmark'
            Bookmark_list = Bookmark.objects.filter(User_ID=user.User_ID).order_by('-id')
            feed_list = []
            for bookmark in Bookmark_list:
                feed_list.append({
                    'feed_img' : Feed.objects.filter(id=bookmark.content_id).first().feed_img,
                    'id' : Feed.objects.filter(id=bookmark.content_id).first().id
                })
        return render(request, 'user/profile.html', context=dict(user=user, feed_list=feed_list, feed_list_count=len(Feed.objects.filter(User_ID=user.User_ID)), now_searchname=now_searchname))
    
    def post(self,request):
        user = User.objects.filter(User_ID=request.session.get('User_ID')).first()
        
        user.nickname = request.data.get('nickname')
        user.name = request.data.get('name')
        user.profile_comment = request.data.get('profile_comment')

        profile_image = request.data.get('profile_image')

        # 프로필이미지 이름을 넘겨 받은 경우
        if profile_image != None:
            if profile_image == "/media/profile_image/default_profile.jpeg": # 기본프사 주소를 넘겨받음: 기본프사를 원한다는뜻이므로 기본프사로 바꾸어준다
                if user.profile_image != "/media/profile_image/default_profile.jpeg": # 기존에 기본프사인지 검사하여 기본프사가 아니었을 경우 기존 프사 파일을 삭제하고 기본프사로 바꾼다, 이미 기본프사였다면 수정할 필요가 없다
                    os.remove(os.path.join(MEDIA_ROOT, user.profile_image[7:]))
                    user.profile_image = profile_image
            else: # 기본프사로 넘겨받지 않은 경우 (새로운 프사를 업로드했다는뜻)    
                if user.profile_image == "/media/profile_image/default_profile.jpeg": # 기존에 기본프사인경우: 커스텀프사 주소가 존재하지않으므로 만들어준다
                    uuid_name = uuid4().hex + profile_image
                    save_path = os.path.join(MEDIA_ROOT, ("profile_image/" + uuid_name))
                    user.profile_image = "/media/profile_image/" + uuid_name
                else: # 기존부터 커스텀프사를 사용중인경우 : 기존프사에 덫씌우기 위해 같은 이름으로 경로를 지정해준다
                    save_path = os.path.join(MEDIA_ROOT, user.profile_image[7:])
                file = request.FILES['file']
                with open(save_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                    
        user.save()
        return Response(status=200)


class join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        User_ID = request.data.get('User_ID')
        name = request.data.get('name')
        nickname = request.data.get('nickname')
        password = request.data.get('password')
        User.objects.create(User_ID=User_ID,name=name, nickname=nickname, password=make_password(password),profile_comment="", profile_image="/media/profile_image/default_profile.jpeg")
        return Response(status=200)


class login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        User_ID = request.data.get('User_ID', None)
        password = request.data.get('password', None)
        user = User.objects.filter(User_ID=User_ID).first() # db에 일치하는 id가 있는지 검사
        
        if user != None:
            if user.check_password(password):
                request.session['User_ID'] = User_ID
                print('로그인했습니다. :', request.session['User_ID'])
                return Response(status=200)
            else:
                print('비밀번호가 잘못되었습니다. :', User_ID,'로 시도했음.')
                return Response(status=400, data='로그인 실패(비밀번호)')
        else:
            print('User_ID가 잘못되었습니다.')
            return Response(status=400, data='로그인 실패(아이디)')

        # return Response값으로 data='유저아이디잘못' 으로 줄경우
        # html에서 data['responseJSON'] 으로 뽑을 수 있고
        # data=dict(message='유저아이디잘못') 으로 줄경우
        # data['responseJSON']['message'] 로 뽑을 수 있음.

        # if user == None: # id를 체크하여 없으면 400에러를 리턴
        #     print('User_ID가 잘못되었습니다.')
        #     return Response(status=400)
        # elif user.check_password(password): # 
        #     request.session['User_ID'] = User_ID
        #     print('로그인했습니다. :', request.session['User_ID'])
        #     return Response(status=200)
        # else:
        #     print('비밀번호가 잘못되었습니다. :', User_ID,'로 시도했음.')
        #     return Response(status=400)

class logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')


class delete_feed(APIView):
    def post(self, request):
        content_id = request.data.get('profile_feed_id')
        # Feed 데이터 삭제
        profile_feed_id = Feed.objects.filter(id=content_id).first()
        os.remove(os.path.join(MEDIA_ROOT, profile_feed_id.feed_img[7:]))
        profile_feed_id.delete()

        # Bookmark, Like, Reply 데이터 삭제 : 해당 게시글 관련 데이터를 모두 삭제해주기 위하여
        Bookmark.objects.filter(content_id=content_id).delete()
        Like.objects.filter(content_id=content_id).delete()
        Reply.objects.filter(content_id=content_id).delete()
        
        return Response(status=200)


class update_feed(APIView):
    def post(self, request):
        feed = Feed.objects.filter(id=request.data.get('content_id')).first()
        feed.feed_content = request.data.get('feed_content')
        file = request.FILES

        if len(file) == 1: # 파일을 넘겨받은 경우 딕셔너리의 길이가 1이 됨 그래서 파일 존재유무를 구분
            save_path = os.path.join(MEDIA_ROOT, feed.feed_img[7:]) # 존재할경우 기존 저장된 경로위 덫씌운다
            with open(save_path, 'wb+') as destination:
                for chunk in file['file'].chunks():
                    destination.write(chunk)
        feed.save()

        return Response(status=200)


class verify_pw(APIView):
    def post(self, request):
        user = User.objects.filter(User_ID=request.session['User_ID']).first()
        password = request.data.get('verify_pw')
        if user.check_password(password):
            request.session['pass'] = 1
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message='비밀번호 불일치'))


class change_account(APIView):
    def get(selft, request):
        user = User.objects.filter(User_ID=request.session.get('User_ID')).first()
        if user == None:
            return render(request, 'user/login.html')

        if request.session['pass'] == 1:
            request.session['pass'] = 0
            request.session['delete_pass'] = 1
            return render(request, 'user/change_account.html')
        else:
            return profile.get(profile, request)

    def post(self, request):
        user = User.objects.filter(User_ID=request.session['User_ID']).first()

        NOW_PASSWORD = request.data.get('NOW_PASSWORD')
        if user.check_password(NOW_PASSWORD) == False:
            return Response(status=400, data='현재 비밀번호가 일치하지 않습니다.')

        NEW_PASSWORD = request.data.get('NEW_PASSWORD')
        NEW2_PASSWORD = request.data.get('NEW2_PASSWORD')
        if NEW_PASSWORD != NEW2_PASSWORD:
            return Response(status=400, data='새로운 비밀번호가 일치하지 않습니다.')

        if NOW_PASSWORD == NEW_PASSWORD:
            return Response(status=400, data='기존 비밀번호는 사용할 수 없습니다.')

        user.password = make_password(NEW_PASSWORD)
        user.save()
        request.session.flush()
        return Response(status=200)


class delete_account(APIView):
    def get(self, request):
        user = User.objects.filter(User_ID=request.session.get('User_ID')).first()
        if user == None:
            return render(request, 'user/login.html')

        if request.session['delete_pass'] == 1:
            request.session['delete_pass'] = 0
            return render(request, 'user/delete_account.html')
        else:
            return profile.get(profile, request)
            
    def post(self,request):
        user = User.objects.filter(User_ID=request.session.get('User_ID')).first()
        PASSWORD = request.data.get('PASSWORD')
        if user.check_password(PASSWORD) == False:
            return Response(status=400, data='비밀번호가 일치하지 않습니다.')

        User_ID = user.User_ID

        # 내 게시글에 달린 좋아요 북마크 댓글 삭제 후 해당 게시글 삭제
        for feed in Feed.objects.filter(User_ID=User_ID):
            Like.objects.filter(content_id=feed.id).delete()
            Bookmark.objects.filter(content_id=feed.id).delete()
            Reply.objects.filter(content_id=feed.id).delete()
            os.remove(os.path.join(MEDIA_ROOT, feed.feed_img[7:]))
            feed.delete()

        # 내가 누른 좋아요 북마크 댓글 삭제
        Like.objects.filter(User_ID=User_ID).delete()
        Bookmark.objects.filter(User_ID=User_ID).delete()
        Reply.objects.filter(User_ID=User_ID).delete()
        
        # 계정 삭제
        if user.profile_image != "/media/profile_image/default_profile.jpeg":
            os.remove(os.path.join(MEDIA_ROOT, user.profile_image[7:]))
        user.delete()

        request.session.flush()
        return Response(status=200)