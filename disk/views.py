# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import json

from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render
from models import DiskInfo

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
    return render(request, "disk/file_manger.html")

def createFile(request):
    return render(request, "disk/create_file.html")