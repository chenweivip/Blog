# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 11:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20171122_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name_plural': '博客个人分类表'},
        ),
    ]
