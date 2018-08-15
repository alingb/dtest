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
def produceDetail(req):
    host = Host.objects.all()[1:500]
    data = list()
    for each in host:
        eachdata = dict()
        eachdata["sn"] = each.sn
        eachdata["sn_1"] = each.sn_1
        eachdata["bios"] = each.bios
        eachdata["bmc"] = each.bmc
        eachdata["name"] = each.name
        data.append(eachdata)

    resultBean = dict()
    resultBean["code"] = 200
    resultBean["msg"] = 'success'
    resultBean["data"] = data
    return JsonResponse(resultBean)
