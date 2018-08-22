# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-21 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiskInfo',
            fields=[
                ('disk_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('disk_name', models.CharField(max_length=255, verbose_name='\u540d\u5b57')),
                ('disk_type', models.CharField(max_length=255, verbose_name='\u7c7b\u578b')),
                ('disk_size', models.CharField(max_length=255, verbose_name='\u603b\u5927\u5c0f')),
                ('disk_used', models.CharField(max_length=255, verbose_name='\u4f7f\u7528')),
                ('disk_avail', models.CharField(max_length=255, verbose_name='\u53ef\u7528')),
                ('disk_mount', models.CharField(max_length=255, verbose_name='\u6302\u8f7d')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('disk_time', models.CharField(blank=True, max_length=250, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
        ),
    ]
