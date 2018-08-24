# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


@login_required
def index(req):
    return render(req, "html/index.html")


def logout_user(req):
    logout(req)
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
