# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json
import time

from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from models import *

# Create your views here.



def disk(request):
    disk_info = DiskInfo.objects.all()
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    lenth = len(disk_info)
    if not offset or not limit:
        host = disk_info
    else:
        offset = int(offset)
        limit = int(limit)
        host = disk_info[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=["disk_id",
                                                "disk_name", "disk_type",
                                                "disk_size", "disk_used",
                                                "disk_avail", "disk_mount",]))
    print(data)
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def base(request):
    return render(request, "disk/index.html")


def fileManger(request):
    username = request.user
    print(username)
    file = FileManger.objects.filter(file_user=username)
    print(file)
    return render(request, "disk/file_manger.html", {"file": file})


def createFile(request):
    return render(request, "disk/create_file.html")


def groupInfo(request):
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    host = FileGroup.objects.all()
    lenth = len(host)
    if not offset or not limit:
        host = host
    else:
        offset = int(offset)
        limit = int(limit)
        host = host[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=["user_name", "group_name"]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


DISK_TYPE = {
    '1': u'本地盘',
    '2': u'网络盘',
}

def changeFile(request):
    if request.POST:
        msg = eval(request.POST.get("data"))
        username = request.user
        try:
            route = msg["route"]
            print(route)
            file = FileManger.objects.get(route=route)
            print("error")
            return HttpResponseBadRequest()
        except:
            file = FileManger()
        file.file_group = msg["file_group_name"]
        file.file_disk_type = DISK_TYPE[msg["file_disk_type"]]
        file.file_disk_name = msg["file_disk_name"]
        file.file_route = msg["file_route"]
        file.file_share_name = msg["file_share_name"]
        file.file_cold_time = msg["file_cold_time"]
        file.file_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        file.file_user = username
        file.save()
        return HttpResponse("name")
    else:
        username = request.user
        file = FileManger.objects.filter(file_user=username)
        print(file)
        return render(request, "disk/file_manger.html", {"file": file})


def gropupChange(request):
    if request.POST:
        msg = eval(request.POST.get("data"))
        groupname = msg["group"]
        username = request.user
        try:
            FileGroup.objects.get(group_name=groupname)
            return HttpResponseBadRequest()
        except:
            group = FileGroup()
        group.group_name = groupname
        group.user_name = username
        group.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("error")