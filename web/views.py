# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse


@login_required
def index(req):
    return render(req, "html/index.html")


def logout_user(req):
    logout(req)
    return redirect(reverse('login'))


def check_password(passwd):
    if re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$',passwd):
        return True
    else:
        return False


def signup(request):
    if request.method == "GET":
        return render(request, 'web/signup.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        rpassword = request.POST.get('checkpassword', None)
        try:
            User.objects.get(username=username)
            return render(request, 'web/signup.html', {"error": u'用户已注册!'})
        except:
            pass
        if rpassword != password:
            return render(request, 'web/signup.html', {"error": u"两次密码输入不一样"})
        if not check_password(password):
            return render(request, 'web/signup.html', {"error": u"password  is invalid"})
        passwd = make_password(password)
        User.objects.create(username=username,
                            password=passwd,
                            is_active=True,
                            is_staff=True)
        return redirect(reverse('login'))


def login_user(request):
    if request.method == 'GET':
        return render(request, 'web/login.html')
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember = request.POST.get('remember', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            return redirect(reverse('index'))
        else:
            return render(request, 'web/login.html', {'error': u'用户名或密码错误!'})


@login_required
def base(req):
    return render(req, 'web/index.html')


def get_info(req):
    from detail.models import CpuStat
    cpu_stat = CpuStat.objects.all()
    data = []
    for each in cpu_stat:
        data.append([int(each.now_time), float(each.cpu_stat),
                    float(each.cpu_stat) + 1, float(each.cpu_stat) + 2])
    return HttpResponse(json.dumps(data))
