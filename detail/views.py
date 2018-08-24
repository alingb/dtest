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
        data.append(model_to_dict(each, fields=["fru", "family", "ip", "sn", "sn_1", "bios", "bmc", "name"]))
    return HttpResponse(json.dumps({"rows": data, "total": lenth}))


def change(req):
    if req.POST:
        info = req.POST.get("data")
        print info
        return HttpResponse(json.dumps({"status": 200, "data": "sucess"}), content_type="application/json")
    else:
        return HttpResponse("fail")