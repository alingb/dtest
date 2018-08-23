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
    disk_add_time = models.DateTimeField('提交时间', auto_now_add=True)
    disk_disk_time = models.CharField('更新时间', max_length=250, blank=True)


class FileManger(models.Model):
    file_disk_type = models.CharField('硬盘类型', max_length=255)
    file_route = models.CharField('文件路径', max_length=255)
    file_share_name = models.CharField('共享名称', max_length=255)
    file_disk_name = models.CharField("硬盘名称", max_length=255)
    file_cold_time = models.CharField("冻结时间", max_length=255)
    file_add_time = models.DateTimeField('提交时间', auto_now_add=True)
    file_time = models.CharField('更新时间', max_length=255)
    file_user = models.CharField('用户', max_length=255, default='--')
    file_group = models.CharField('群组', max_length=255, default='--')


class FileGroup(models.Model):
    group_name = models.CharField('群组名称', max_length=255)
    user_name = models.CharField('用户', max_length=255)