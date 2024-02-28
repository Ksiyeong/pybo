from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from common.models import Profile



class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')
    class Meta:
        model = User  # 사용할 모델
        fields = ('username', 'email', 'password1', 'password2')  # UserForm에서 사용할 User 모델의 속성


class Profile_ModifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['introduction', 'bloodtype']
        labels = {
            'introduction': '자기소개',
            'bloodtype': '혈액형'
        }