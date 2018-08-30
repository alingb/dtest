# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class DiskInfo(models.Model):
    disk_id = models.IntegerField('ID', primary_key=True)
    disk_name = models.CharField('名字', max_length=255)
    disk_type = models.CharField('类型', max_length=255)
    disk_size = models.CharField('总大小', max_length=255)
    disk_used = models.CharField('使用', max_length=255)
    disk_avail = models.CharField('可用', max_length=255)
    disk_mount = models.CharField('挂载目录', max_length=255)
    disk_add_time = models.DateTimeField('提交时间', auto_now_add=True)
    disk_disk_time = models.CharField('更新时间', max_length=250, blank=True)
    disk_back_stat = models.IntegerField('备用盘状态', default=0)
    disk_use_stat = models.IntegerField('使用状态', default=0)


class FileManger(models.Model):
    file_disk_type = models.CharField('硬盘类型', max_length=255)
    file_route = models.CharField('文件路径', max_length=255)
    file_share_name = models.CharField('共享名称', max_length=255)
    file_disk_name = models.CharField("硬盘名称", max_length=255)
    file_cold_time = models.CharField("冻结时间", max_length=255)
    file_add_time = models.DateTimeField('提交时间', auto_now_add=True)
    file_time = models.CharField('更新时间', max_length=255, default=timezone.now)
    file_user = models.CharField('用户', max_length=255, default='--')
    file_group = models.CharField('群组', max_length=255, default='--')
    file_active_stat = models.CharField('激活状态', max_length=255, default=u"未激活")
    file_share_stat = models.CharField("共享状态", max_length=255, default=u"未共享")
    file_full_route = models.CharField("存储路径", max_length=255, default="")


class Group(models.Model):
    name = models.CharField('群组名称', max_length=255)

    def __str__(self):
        return self.name


class FileGroup(models.Model):
    user_name = models.CharField('用户', max_length=255)
    group_name = models.ForeignKey(Group, related_name="group_user", on_delete=models.CASCADE, default="")


class DiskStat(models.Model):
    disk_name = models.CharField("名称", max_length=255, default="-")
    disk_stat_name = models.CharField("盘符", max_length=255)
    disk_stat = models.CharField("状态", max_length=255)
    disk_slot = models.IntegerField("编号")
    disk_off_stat = models.IntegerField("关闭状态", default=0)
    disk_uuid = models.CharField("UUID", max_length=255, blank=True)


class FileUpload(models.Model):
    username = models.CharField("用户", max_length=255, blank=True)
    groupname = models.CharField("群组", max_length=255, blank=True)
    filename = models.CharField("文件名称", max_length=255, blank=True)
    route = models.CharField("路径", max_length=255, blank=True)
    cold_time = models.CharField("冻结时间", max_length=255, blank=True)
    stat = models.IntegerField("状态", default=0)
    file = models.FileField("附件上传", default='')
    file_full_route = models.CharField("传输路径", max_length=255, default='')
    file_add_time = models.DateTimeField("上传时间", auto_now_add=True)


class UploadDownFile(models.Model):
    file = models.FileField("附件上传", default='')
