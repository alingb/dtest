# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CpuStat(models.Model):
    now_time = models.CharField(max_length=255)
    cpu_stat = models.CharField(max_length=255)
