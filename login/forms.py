from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class 自定义注册表单(UserCreationForm):
    昵称 = forms.CharField(max_length=50, required=False)
    生日 = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', '昵称', '生日')


class 自定义编辑表单(UserChangeForm):
    昵称 = forms.CharField(max_length=50, required=False)
    生日 = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', '昵称', '生日')
