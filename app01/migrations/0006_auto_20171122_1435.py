# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20171121_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='siteCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='app01.SiteCategory', verbose_name='所属博客系统分类'),
        ),
    ]
