# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import FileManger
# Register your models here.


class FileMangerAdmin(admin.ModelAdmin):
    pass


admin.site.register(FileManger)