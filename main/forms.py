from django import forms
from main.models import Diary


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary  # 사용할 모델
        fields = ['subject', 'content']  # DiaryForm에서 사용할 Diary 모델의 속성

        labels = {
            'subject': '제목', # 필드명 보여줄때 지정가능
            'content': '내용',
        } 