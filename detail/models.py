# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CpuStat(models.Model):
    add_time = models.CharField("时候", max_length=255)
    stat = models.CharField("状态", max_length=255)


class MemStat(models.Model):
    add_time = models.CharField("时间", max_length=255)
    stat = models.CharField("状态", max_length=255)


class NetworkStat(models.Model):
    add_time = models.CharField("时间", max_length=255)
    name = models.CharField("名称", max_length=255)
    on_stat = models.CharField("上传状态", max_length=255)
    down_stat = models.CharField("下载状态", max_length=255)


class CpuLoad(models.Model):
    add_time = models.CharField("时间", max_length=255)
    one_time_stat = models.CharField("1分钟状态", max_length=255)
    five_time_stat = models.CharField("5分钟状态", max_length=255)
    fifteen_time_stat = models.CharField("15分钟状态", max_length=255)