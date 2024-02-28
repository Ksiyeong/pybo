from django.shortcuts import render
from user.models import User
from .models import Feed, Reply, Like, Bookmark
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from uuid import uuid4
from 인스타클론.settings import MEDIA_ROOT

# def index(request):
#     User_ID = request.session.get('User_ID')
#     User.objects.filter(User_ID=User_ID).first()
#     if User_ID == None:
#         return render(request, 'user/login.html')
#     else:
#         return render(request, 'main/main.html')

def index(request):
    user = User.objects.filter(User_ID=request.session.get('User_ID')).first()
    if user == None:
        return render(request, 'user/login.html')

    feed_list = []
    Feed_objects_list = Feed.objects.all().order_by('-id')
    for feed in Feed_objects_list:
        user2 = User.objects.filter(User_ID=feed.User_ID).first()
        is_liked = Like.objects.filter(User_ID=user.User_ID, content_id=feed.id).exists()
        is_bookmarked = Bookmark.objects.filter(User_ID=user.User_ID, content_id=feed.id).exists()
        like_users = Like.objects.filter(content_id=feed.id)
        reply_count = len(Reply.objects.filter(content_id=feed.id))

        feed_list.append({
            'id' : feed.id,
            'nickname' : user2.nickname,
            'profile_image' : user2.profile_image,
            'feed_img' : feed.feed_img,
            'feed_content' : feed.feed_content,
            'is_liked' : is_liked,
            'is_bookmarked' : is_bookmarked,
            'like_count' : len(like_users) -1,
            'reply_count' : reply_count
        })
        if like_users.first() != None:
            like_user = User.objects.filter(User_ID=like_users.first().User_ID).first()
            feed_list[-1]['like_user'] = like_user.nickname
            feed_list[-1]['like_user_profile_image'] = like_user.profile_image
        
    reply_list = []
    Reply_objects_list = Reply.objects.all()
    for Reply_object in Reply_objects_list:
        user_reply = User.objects.filter(User_ID=Reply_object.User_ID).first()
        reply_list.append({
            'content_id' : int(Reply_object.content_id),
            'nickname' : user_reply.nickname,
            'reply' : Reply_object.reply
        })

    return render(request, 'main/main.html', context=dict(user=user, feed_list=feed_list, reply_list=reply_list))


class feed_upload(APIView):
    def post(self, request):
        User_ID = request.session["User_ID"]
        feed_img = request.data.get('feed_img')
        feed_content = request.data.get('feed_content')

        file = request.FILES['file']
        uuid_name = uuid4().hex + feed_img

        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        Feed.objects.create(User_ID=User_ID,feed_img="/media/" + uuid_name, feed_content=feed_content)
        return Response(status=200)


class reply_upload(APIView):
    def post(self, request):
        content_id = request.data.get('content_id')
        User_ID = request.session["User_ID"]
        reply = request.data.get('reply')

        Reply.objects.create(content_id=content_id, User_ID=User_ID, reply=reply)
        return Response(status=200)


class like_content(APIView):
    def post(self, request):
        content_id = request.data.get('content_id')
        User_ID = request.session["User_ID"]
        distinct = Like.objects.filter(content_id=content_id, User_ID=User_ID).first()
        if distinct:
            distinct.delete()
        else:
            Like.objects.create(content_id=content_id, User_ID=User_ID)
        return Response(status=200)

    
class bookmark_content(APIView):
    def post(self, request):
        content_id = request.data.get('content_id')
        User_ID = request.session["User_ID"]
        distinct = Bookmark.objects.filter(content_id=content_id, User_ID=User_ID).first()
        if distinct:
            distinct.delete()
        else:
            Bookmark.objects.create(content_id=content_id, User_ID=User_ID)
        return Response(status=200)