# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import re
from subprocess import Popen, PIPE

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse
from detail.models import *


@login_required
def index(req):
    return render(req, "html/index.html")


def logout_user(req):
    logout(req)
    return redirect(reverse('login'))


def check_password(passwd):
    if re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$', passwd):
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


@login_required
def cpuStat(req):
    return render(req, 'web/cpustat.html')


@login_required
def memStat(req):
    return render(req, 'web/memstat.html')


@login_required
def diskStat(req):
    return render(req, 'web/diskstat.html')


@login_required
def logStat(req):
    return render(req, 'web/logstat.html', )


@login_required
def netStat(req, netname):
    netstat = NetworkStat.objects.values('name')
    name_list = []
    for name in netstat:
        name_list.append(name['name'])
    name = list(set(name_list))
    if not netname and name:
        netname = name[0]
    else:
        netname = ''
    return render(req, 'web/netstat.html', {"name": name, "netname": netname})


def get_info(req, getname):
    if getname == 'cpu':
        cpu_stat = CpuStat.objects.all()
        data = []
        for each in cpu_stat:
            data.append([int(each.add_time), float(each.stat)])
        return HttpResponse(json.dumps(data))
    elif getname == 'mem':
        mem_stat = MemStat.objects.all()
        data = []
        for each in mem_stat:
            data.append([int(each.add_time), float(each.stat)])
        return HttpResponse(json.dumps(data))
    elif "on" in getname:
        netname = getname.split("_")[0]
        net_stat = NetworkStat.objects.filter(name=netname)
        data = []
        for each in net_stat:
            data.append([int(each.add_time), float(each.on_stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif "down" in getname:
        netname = getname.split("_")[0]
        net_stat = NetworkStat.objects.filter(name=netname)
        print(net_stat)
        data = []
        for each in net_stat:
            data.append([int(each.add_time), float(each.down_stat)])
        sorted(data)
        return HttpResponse(json.dumps(data))
    elif getname == 'loginfo':
        log_list, log_dict, lenth = [], {}, 0
        try:
            popen = Popen(r'ipmitool sel list', stdout=PIPE, stderr=PIPE, shell=True)
            info = popen.stdout.readlines()
            for msg in info:
                data = msg.split('|')
                log_dict['id'] = data[0]
                log_dict['time'] = data[1] + data[2]
                if '/' in data[3]:
                    log_msg = data[3].split('/')
                    log_dict['name'] = log_msg[0]
                    log_dict['type'] = log_msg[1]
                else:
                    log_msg = data[3].split('#')
                    log_dict['name'] = log_msg[1]
                    log_dict['type'] = log_msg[0]
                log_dict['desc'] = data[4] + '-' + data[5]
                log_list.append(log_dict)
            lenth = len(log_list)
            if not log_list:
                raise Exception('error')
        except:
            log_list = [{'id': 1, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'type': 'error',
                         'desc': 'no data', 'name': 'ipmi error'}]
            lenth = 1
            return HttpResponse(json.dumps({"rows": log_list, "total": lenth}))
        return HttpResponse(json.dumps({"rows": log_list, "total": lenth}))

