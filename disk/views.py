# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import hashlib
import json

import time
from subprocess import Popen, PIPE

from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from models import *
from forms import FileUploadDown

# Create your views here.


def diskInfo(request):
    disk_stat = 1
    disk_info = DiskInfo.objects.filter(disk_use_stat=disk_stat)
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
                                                "disk_avail", "disk_mount"]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def diskAdd(request):
    add_stat = 0
    disk_info = DiskInfo.objects.filter(disk_use_stat=add_stat)
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
                                                "disk_avail", "disk_mount", ]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def fileInfo(request):
    username = request.user
    file_info = FileManger.objects.filter(file_user=username)
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    lenth = len(file_info)
    if not offset or not limit:
        host = file_info
    else:
        offset = int(offset)
        limit = int(limit)
        host = file_info[offset:offset + limit]
    data = []
    for each in host:
        dict = model_to_dict(each)
        dict.update({"file_add_time": each.file_add_time.strftime("%Y-%m-%d %H:%M:%S")})
        data.append(dict)
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def diskBack(request):
    add_stat = 0
    back_stat = 0
    disk_info = DiskInfo.objects.filter(disk_use_stat=add_stat)
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
                                                "disk_avail", "disk_mount", ]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def base(request):
    return render(request, "disk/index.html")


def diskAddInfo(request):
    return render(request, "disk/diskadd.html")


def fileManger(request):
    username = request.user
    file = FileManger.objects.filter(file_user=username)
    return render(request, "disk/file_manger.html", {"file": file})


def createFile(request):
    disk_stat = 1
    disk_info = DiskInfo.objects.filter(disk_use_stat=disk_stat)
    return render(request, "disk/create_file.html", {"info": disk_info})


def diskBack(request):
    return render(request, "disk/disk_backup.html")


def fileDetail(request, id):
    if request.method == "POST":
        try:
            file = FileUploadDown(request.POST, request.FILES)
            file_manger = FileManger.objects.get(id=id)
            myFile = request.FILES.get("file", None)
            if file.is_valid():
                upfile = FileUpload()
                upfile.file = file.cleaned_data["file"]
                upfile.username = file_manger.file_user
                upfile.groupname = file_manger.file_group
                upfile.filename = myFile.name
                upfile.route = file_manger.file_route
                upfile.file_full_route = file_manger.file_full_route
                upfile.cold_time = file_manger.file_cold_time
                upfile.save()
                return HttpResponseRedirect('/disk/file/{}/'.format(id))
            else:
                return render(request, "disk/file_detail.html", {"file": file})
        except Exception as e:
            return HttpResponse(e)
    else:
        file_manger = FileManger.objects.get(id=id)
        username = file_manger.file_user
        groupname = file_manger.file_group
        route = file_manger.file_route
        file_list = []
        try:
            file_ipload_stat = FileUpload.objects.filter(username=username, groupname=groupname, route=route)
            for file_each in file_ipload_stat:
                file_dict = model_to_dict(file_each)
                file_dict.update({"file_add_time": file_each.file_add_time.strftime("%Y-%m-%d %H:%M:%S")})
                file_list.append(file_dict)
        except Exception as e:
            raise e
        return render(request, "disk/file_detail.html", {"file": file_manger, "file_msg": file_list})


def groupInfo(request):
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    host = Group.objects.all()
    lenth = len(host)
    if not offset or not limit:
        host = host
    else:
        offset = int(offset)
        limit = int(limit)
        host = host[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=["id", "name"]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


DISK_TYPE = {
    '1': u'本地盘',
    '2': u'网络盘',
}


def changeFile(request):
    if request.POST:
        msg = eval(request.POST.get("data"))
        username = request.user
        groupname = msg["file_group_name"]
        group = Group.objects.get(name=groupname)
        group_id = group.id
        try:
            FileGroup.objects.get(user_name=username, group_name_id=group_id)
        except:
            file_group = FileGroup()
            file_group.user_name = username
            file_group.group_name_id = group_id
            file_group.save()
        try:
            route = msg["route"]
            FileManger.objects.get(route=route)
            return HttpResponseBadRequest()
        except:
            file = FileManger()
        file.file_group = groupname
        file.file_disk_type = DISK_TYPE[msg["file_disk_type"]]
        file.file_disk_name = msg["file_disk_name"]
        file.file_route = msg["file_route"]
        file.file_share_name = msg["file_share_name"]
        file.file_cold_time = msg["file_cold_time"]
        file.file_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.file_user = username
        if "/" in msg["file_route"]:
            file.file_full_route = "/{}/{}{}".format(msg["file_group_name"], username, msg["file_route"])
        else:
            file.file_full_route = "/{}/{}/{}".format(msg["file_group_name"], username, msg["file_route"])
        file.save()
        return HttpResponse()
    else:
        username = request.user
        file = FileManger.objects.filter(file_user=username)
        return render(request, "disk/file_manger.html", {"file": file})


def gropupChange(request):
    if request.POST:
        msg = eval(request.POST.get("data"))
        groupname = msg["group"]
        username = request.user
        try:
            Group.objects.get(name=groupname)
            return HttpResponseBadRequest()
        except:
            group = Group()
        group.name = groupname
        group.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def chechRoute(request):
    if request.POST:
        msg = request.POST.get("data")
        route = eval(msg)["route"]
        username = request.user
        try:
            FileManger.objects.get(file_user=username, file_route=route)
        except:
            return HttpResponse("ok")
        return HttpResponseBadRequest()


def changeFileInfo(request):
    if request.POST:
        post_msg = request.POST.get("data")
        msg = eval(post_msg)["msg"]
        msg_id = eval(post_msg)["id"]
        if "disk" in msg:
            for id in msg_id:
                disk = DiskInfo.objects.get(disk_id=id)
                if msg == "disk_add":
                    disk.disk_use_stat = 1
                    disk.save()
                if msg == "disk_del":
                    disk.disk_use_stat = 0
                    disk.save()
        else:
            for id in msg_id:
                file = FileManger.objects.get(id=id)
                if msg == "active_change":
                    if file.file_active_stat == "未激活":
                        file.file_active_stat = u"激活"
                    else:
                        file.file_active_stat = u"未激活"
                    file.save()
                if msg == "change_share":
                    if file.file_share_stat == "未共享":
                        file.file_share_stat = u"开启"
                    else:
                        file.file_share_stat = u"未共享"
                    file.save()
                if msg == "change_smb":
                    pass
                if msg == "file_del":
                    file.delete()
        return HttpResponse("")


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def changeData(request):
    if request.POST:
        post_msg = request.POST.get("data")
        msg = eval(post_msg)["msg"]
        msg_id = eval(post_msg)["id"].split("_")[1]
        file = FileUpload.objects.get(id=msg_id)
        if msg == "delete":
            file.file.delete()
            file.delete()
            return HttpResponse()
    elif request.GET:
        id = request.GET['url'].split("_")[1]
        file = FileUpload.objects.get(id=id)
        try:
            file_route = file.file.path
        except:
            file_route = file.file_full_route
        response = FileResponse(file_iterator(file_route))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file.filename)
        return response


def diskControl(request):
    if request.method == "POST":
        post_msg = eval(request.POST.get("data"))
        msg = post_msg["msg"]
        id = post_msg["id"]
        name = post_msg["name"]
        if msg == "start":
            for i in name:
                num, disk_name =  i.split(':')
                var = Popen(r'/bin/disk_cotrol -o {} -d {}'.format(num, disk_name), stdout=PIPE, stderr=PIPE, shell=True)
                var.communicate()
                var.returncode

            # for i in id:
            #     disk = DiskStat.objects.get(id=i)
            #     if disk.disk_off_stat == 0:
            #         continue
            #     else:
            #         disk.disk_off_stat = 0
            #     disk.disk_stat = "OK"
            #     disk.save()
            return HttpResponse()
        if msg == "stop":
            for i in name:
                num, disk_name =  i.split(':')
                var = Popen(r'/bin/disk_cotrol -c {} -d {}'.format(num, disk_name), stdout=PIPE, stderr=PIPE, shell=True)
                var.communicate()
                var.returncode

            # for i in id:
            #     disk = DiskStat.objects.get(id=i)
            #     if disk.disk_off_stat == 1:
            #         continue
            #     else:
            #         disk.disk_off_stat = 1
            #     disk.disk_stat = "OFF"
            #     disk.save()
            return HttpResponse()
    else:
        return render(request, "disk/disk_control.html")


def diskMangerInfo(request):
    if request.GET:
        var = Popen(r'storge_stat', stdout=PIPE, stderr=PIPE, shell=True)
        var.communicate()
        var.returncode
        file_info = DiskStat.objects.all()
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        lenth = len(file_info)
        if not offset or not limit:
            host = file_info
        else:
            offset = int(offset)
            limit = int(limit)
            host = file_info[offset:offset + limit]
        data = []
        for each in host:
            dict = model_to_dict(each)
            data.append(dict)
        return HttpResponse(json.dumps({"rows": data, "total": lenth}))
    elif request.method == "POST":
        msg = json.loads(request.body)
        for key, value in msg.items():
            try:
                file_info = DiskStat.objects.get(disk_stat_name=key)
            except:
                file_info = DiskStat()
            file_info.disk_stat_name = key
            file_info.disk_stat = value['status']
            file_info.disk_slot = int(value['slot'])
            file_info.disk_slot = value['slot']
            file_info.disk_off_stat = value['off']
            file_info.disk_uuid = value['UUID']
            file_info.save()
        return HttpResponse()
    else:
        return HttpResponse()

from django.contrib.auth.hashers import make_password, check_password