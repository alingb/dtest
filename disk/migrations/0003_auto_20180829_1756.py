# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-29 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0002_diskstat_disk_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileGroup1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='FileGroup',
            new_name='FileUser',
        ),
        migrations.AddField(
            model_name='filegroup1',
            name='group_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='group_user', to='disk.FileUser'),
        ),
    ]
