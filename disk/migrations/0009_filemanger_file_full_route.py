# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-24 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0008_auto_20180824_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemanger',
            name='file_full_route',
            field=models.CharField(default='', max_length=255, verbose_name='\u5b58\u50a8\u8def\u5f84'),
        ),
    ]
