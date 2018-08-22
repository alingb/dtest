# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class DiskInfo(models.Model):
    disk_id = models.IntegerField('ID', primary_key=True)
    disk_name = models.CharField('名字', max_length=255)
    disk_type = models.CharField('类型', max_length=255)
    disk_size = models.CharField('总大小', max_length=255)
    disk_used = models.CharField('使用', max_length=255)
    disk_avail = models.CharField('可用', max_length=255)
    disk_mount = models.CharField('挂载', max_length=255)
    add_time = models.DateTimeField('提交时间', auto_now_add=True)
    disk_time = models.CharField('更新时间', max_length=250, blank=True)