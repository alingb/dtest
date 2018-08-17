# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from web.models import Host

from django.forms.models import model_to_dict
# Create your views here.


@login_required
def index(req):
    return render(req, 'detail/index.html')


@login_required
def produceDetail(request):
    import time
    start_time = time.time()
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    host = Host.objects.filter(stress_test="running")
    lenth = len(host)
    if not offset or not limit:
        host = host
    else:
        offset = int(offset)
        limit = int(limit)
        host = host[offset:offset + limit]
    data = []
    for each in host:
        data.append(model_to_dict(each, fields=["sn", "sn_1", "bios", "bmc", "name"]))
    end_time = time.time()
    print end_time - start_time
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))
    # host = Host.objects.all()[1:500]
    # data = list()
    # for each in host:
    #     eachdata = dict()
    #     eachdata["sn"] = each.sn
    #     eachdata["sn_1"] = each.sn_1
    #     eachdata["bios"] = each.bios
    #     eachdata["bmc"] = each.bmc
    #     eachdata["name"] = each.name
    #     data.append(eachdata)
    #
    # resultBean = dict()
    # resultBean["code"] = 200
    # resultBean["msg"] = 'success'
    # resultBean["data"] = data
    # return JsonResponse(data)


def change(req):
    if req.POST:
        info = req.POST.get("data")
        return HttpResponse(json.dumps({"status": 200, "data": "sucess"}), content_type="application/json")
    else:
        return HttpResponse("fail")