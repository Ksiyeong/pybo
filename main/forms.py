from django import forms
from main.models import Posts, Reply


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts  # 사용할 모델
        fields = ['category', 'subject', 'content']  # PostsForm에서 사용할 Posts 모델의 속성

        labels = {
            'category': '카테고리',
            'subject': '제목', # 필드명 보여줄때 지정가능
            'content': '내용',
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        labels = {
            'content' : '댓글 내용'
        }