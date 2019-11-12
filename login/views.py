from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import 自定义注册表单, 自定义编辑表单
from .models import 普通会员表
from django.contrib.auth.decorators import login_required


# Create your views here.


def 主页(request):
    return render(request, 'login/home.html')


def 登录(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['用户名'], password=request.POST['密码'])
        if user is None:
            return render(request, 'login/login.html', {'error': "用户名或密码错误"})
        else:
            login(request, user)
            return redirect('login:主页')
    else:
        return render(request, 'login/login.html')


def 登出(request):
    logout(request)
    return redirect('login:主页')


def 注册(request):
    if request.method == 'POST':
        register_form = 自定义注册表单(request.POST)
        if register_form.is_valid():
            register_form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            普通会员表(用户=user, 昵称=request.POST['昵称'], 生日=request.POST['生日']).save()
            login(request, user)
            return redirect('login:主页')
    else:
        register_form = 自定义注册表单()
    content = {'register_form': register_form}
    return render(request, 'login/register.html', content)


@login_required(login_url='login:登录')
def 个人中心(request):
    content = {'user': request.user}
    return render(request, 'login/user_center.html', content)


@login_required(login_url='login:登录')
def 编辑个人信息(request):
    if request.method == 'POST':
        change_form = 自定义编辑表单(request.POST, instance=request.user)
        if change_form.is_valid():
            change_form.save()
            request.user.普通会员表.昵称 = change_form.cleaned_data['昵称']
            request.user.普通会员表.生日 = change_form.cleaned_data['生日']
            request.user.普通会员表.save()
            return redirect('login:个人中心')
    else:
        change_form = 自定义编辑表单(instance=request.user)
    content = {'change_form': change_form, 'user': request.user}
    return render(request, 'login/edit_profile.html', content)


@login_required(login_url='login:登录')
def 修改密码(request):
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if change_password_form.is_valid():
            change_password_form.save()
            return redirect('login:登录')
    else:
        change_password_form = PasswordChangeForm(user=request.user)
    content = {'change_password_form': change_password_form, 'user': request.user}
    return render(request, 'login/change_password.html', content)
